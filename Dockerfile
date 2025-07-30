FROM python:3.12-slim

# Install system dependencies for Chromium and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    unzip \
    curl \
    wget \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:$PORT app:app"]
