# Python बेस इमेज
FROM python:3.10-slim

# काम करने की डायरेक्ट्री
WORKDIR /app

# सिस्टम डिपेंडेंसी (ffmpeg, yt-dlp, aria2, wget)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    aria2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python पैकेज इंस्टॉल करें
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# बाकी कोड कॉपी करें
COPY . .

# बॉट चलाएँ
CMD ["python", "main.py"]
