import os
import re
import sys
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID as api_id
from vars import API_HASH as api_hash
from vars import BOT_TOKEN as bot_token
from vars import OWNER_ID as owner
from vars import SUDO_USERS as sudo_users

from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

bot = Client(
    name=":memory:",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@bot.on_message(filters.command(["start"]))
async def start_cmd(bot: Client, m: Message):
    await m.reply_text(
        "BOT MADE BY - 𓊈𒆜🅲🆁🅰🆉🆈_🅼🅸🅽🅳𒆜𓊉\n\n"
        "I am a Bot For Download Links From Your **TXT** File And Then Upload That File On Telegram"
    )

@bot.on_message(filters.command("stop"))
async def stop_cmd(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload_handler(bot: Client, m: Message):
    editable = await m.reply_text("📂 SEND ME TXT FILE TO DOWNLOAD")
    input_file_msg: Message = await bot.listen(editable.chat.id)
    txt_path = await input_file_msg.download()
    await input_file_msg.delete(True)

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        links_raw = content.split("\n")
        links = []
        for line in links_raw:
            if "://" in line:
                parts = line.split("://", 1)
                if len(parts) == 2:
                    links.append(parts)
        os.remove(txt_path)
    except Exception as e:
        await m.reply_text(f"❌ Invalid file input: {e}")
        os.remove(txt_path)
        return

    await editable.edit(f"Total Links **{len(links)}**\n\nFrom which number to start? (e.g., 1)")
    start_num_msg: Message = await bot.listen(editable.chat.id)
    start_num = int(start_num_msg.text)
    await start_num_msg.delete(True)

    await editable.edit("📝 Now Send Me Your Batch Name")
    batch_msg: Message = await bot.listen(editable.chat.id)
    batch_name = batch_msg.text
    await batch_msg.delete(True)

    await editable.edit("🎥 **Quality**\n144, 240, 360, 480, 720, 1080")
    quality_msg: Message = await bot.listen(editable.chat.id)
    quality = quality_msg.text
    await quality_msg.delete(True)

    quality_map = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }
    res = quality_map.get(quality, "UN")

    await editable.edit("👤 **Download By:** (e.g., Robin)")
    downloader_msg: Message = await bot.listen(editable.chat.id)
    downloader = downloader_msg.text
    await downloader_msg.delete(True)

    await editable.edit("🖼️ **Thumbnail URL** (or type `no` to skip)\nExample: https://graph.org/file/eb18b59310300916efdd0.jpg")
    thumb_msg: Message = await bot.listen(editable.chat.id)
    thumb_input = thumb_msg.text
    await thumb_msg.delete(True)

    await editable.delete()

    thumb = "no"
    if thumb_input.startswith(("http://", "https://")):
        subprocess.run(f'wget -q "{thumb_input}" -O "thumb.jpg"', shell=True)
        if os.path.isfile("thumb.jpg"):
            thumb = "thumb.jpg"
        else:
            thumb = "no"

    count = start_num
    for i in range(start_num - 1, len(links)):
        V = links[i][1].replace("file/d/", "uc?export=download&id=") \
                       .replace("www.youtube-nocookie.com/embed", "youtu.be") \
                       .replace("?modestbranding=1", "") \
                       .replace("/view?usp=sharing", "")
        url = "https://" + V

        if "visionias" in url:
            async with ClientSession() as session:
                async with session.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36'
                }) as resp:
                    text = await resp.text()
                    match = re.search(r"(https://.*?playlist.m3u8.*?)\"", text)
                    if match:
                        url = match.group(1)

        elif 'videos.classplusapp' in url:
            api_resp = requests.get(
                f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}
            )
            if api_resp.status_code == 200:
                url = api_resp.json().get('url', url)

        elif '/master.mpd' in url:
            vid_id = url.split("/")[-2]
            url = f"https://psitoffers.store/testkey.php?vid={vid_id}&quality={quality}"

        name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "") \
                           .replace("+", "").replace("#", "").replace("|", "") \
                           .replace("@", "").replace("*", "").replace(".", "") \
                           .replace("https", "").replace("http", "").strip()
        name = f'{str(count).zfill(3)}) {name1[:60]}'

        if "youtu" in url:
            ytf = f"b[height<={quality}][ext=mp4]/bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
        else:
            ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"

        if "jw-prod" in url:
            cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
        else:
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

        cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}\n\n**Title  »** {name1} {res} 🅲🆁🅰🆉🆈_🅼🅸🅽🅳.mkv\n\n**Batch »** {batch_name}\n\n**Download by »** {downloader}\n\n'
        cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}\n\n**Title »** {name1} 🅲🆁🅰🆉🆈_🅼🅸🅽🅳.pdf \n\n**Batch »** {batch_name}\n\n**Download by »** {downloader}\n\n'

        try:
            if "drive" in url:
                pdf_file = await helper.download_file(url, name)
                if pdf_file:
                    await bot.send_document(chat_id=m.chat.id, document=pdf_file, caption=cc1)
                    os.remove(pdf_file)
                count += 1
                continue

            elif ".pdf" in url:
                pdf_cmd = f'yt-dlp -o "{name}.pdf" "{url}" -R 25 --fragment-retries 25'
                subprocess.run(pdf_cmd, shell=True)
                pdf_file = f"{name}.pdf"
                if os.path.isfile(pdf_file):
                    await bot.send_document(chat_id=m.chat.id, document=pdf_file, caption=cc1)
                    os.remove(pdf_file)
                count += 1
                continue

            else:
                prog = await m.reply_text(
                    f"**⬇️⬇️🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️**\n\n"
                    f"**📝Name »** `{name}`\n❄Quality » {quality}\n\n**🔗URL »** `{url}`"
                )
                video_file = await helper.download_video(url, cmd, name)
                await helper.send_vid(bot, m, cc, video_file, thumb, name, prog)
                count += 1
                time.sleep(1)

        except Exception as e:
            await m.reply_text(
                f"**❌ Download Interrupted**\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
            )
            continue

    await m.reply_text("✅ **Mission Successful**")

bot.run()
