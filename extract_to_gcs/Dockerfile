FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    firefox-esr wget curl unzip \
    libgtk-3-0 libdbus-glib-1-2 libasound2 libx11-xcb1 \
    libnss3 libxrandr2 libxss1 libxtst6 libappindicator1 libnotify-bin \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.33.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt gunicorn flask
CMD ["gunicorn", "-b", ":8080", "main:app"]