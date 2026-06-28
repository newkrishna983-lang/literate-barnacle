import os
import time
import asyncio
import subprocess
import requests
import aiohttp
import aiofiles
import logging

from utils import progress_bar
from pyrogram.types import Message

# --------------------------------------------
# हेल्पर फंक्शन्स
# --------------------------------------------

def duration(filename):
    """ffprobe से वीडियो की अवधि निकाले"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        return float(result.stdout)
    except Exception as e:
        logging.error(f"duration error: {e}")
        return 0

async def download_file(url, name):
    """PDF / ड्राइव लिंक से फ़ाइल डाउनलोड करे"""
    filename = f"{name}.pdf"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, "wb")
                await f.write(await resp.read())
                await f.close()
                return filename
    return None

async def download_video(url, cmd, name):
    """yt-dlp का उपयोग कर वीडियो डाउनलोड करे – रिट्री मैकेनिज्म सहित"""
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
    logging.info(f"Running: {download_cmd}")

    max_retries = 10
    for attempt in range(max_retries):
        proc = subprocess.run(download_cmd, shell=True)
        if proc.returncode == 0:
            break
        logging.warning(f"Attempt {attempt+1} failed, retrying...")
        await asyncio.sleep(5)
    else:
        raise Exception("Download failed after multiple retries")

    output_file = f"{name}.mp4"
    if os.path.isfile(output_file):
        return output_file
    for ext in [".mkv", ".webm", ".mp4.webm"]:
        alt = f"{name}{ext}"
        if os.path.isfile(alt):
            return alt
    raise FileNotFoundError(f"Downloaded file not found for {name}")

async def send_vid(bot, m: Message, caption, filename, thumb, name, prog_msg):
    """वीडियो को थंबनेल के साथ अपलोड करे"""
    if thumb == "no":
        thumb_file = f"{filename}.jpg"
        subprocess.run(
            f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{thumb_file}"',
            shell=True,
            stderr=subprocess.DEVNULL
        )
        if not os.path.isfile(thumb_file):
            thumb_file = None
    else:
        thumb_file = thumb
        if not os.path.isfile(thumb_file):
            thumb_file = None

    await prog_msg.delete()
    reply_msg = await m.reply_text(f"**Uploading ...** - `{name}`")

    dur = int(duration(filename))
    start_time = time.time()

    try:
        await m.reply_video(
            filename,
            caption=caption,
            supports_streaming=True,
            height=720,
            width=1280,
            thumb=thumb_file,
            duration=dur,
            progress=progress_bar,
            progress_args=(reply_msg, start_time)
        )
    except Exception as e:
        logging.error(f"Video upload failed: {e}")
        await m.reply_document(
            filename,
            caption=caption,
            progress=progress_bar,
            progress_args=(reply_msg, start_time)
        )

    if os.path.exists(filename):
        os.remove(filename)
    if thumb_file and thumb_file != thumb and os.path.exists(thumb_file):
        os.remove(thumb_file)
    await reply_msg.delete()
