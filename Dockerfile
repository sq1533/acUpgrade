FROM python:3.12-slim

LABEL description="Monitering Support Systems"
LABEL version="1.0"

WORKDIR /app

# 필수 패키지 업데이트 및 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libxshmfence1 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    libx11-6 \
    libxext6 \
    libxtst6 \
    libxrender1 \
    libxi6 \
    && apt-get clean

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list > /dev/null
RUN apt-get update && apt-get install -y google-chrome-stable

# 모든 파일 복사
COPY . .
# Python 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt