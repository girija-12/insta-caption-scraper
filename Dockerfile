FROM python:3.12-slim

# Install system dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 \
    libnss3 libxss1 libxtst6 libappindicator3-1 libu2f-udev \
    chromium chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variable for headless Chrome
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER="/usr/bin/chromedriver"
ENV DISPLAY=:99

# Set workdir and copy files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]