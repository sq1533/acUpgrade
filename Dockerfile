FROM python:3.12-slim

LABEL description="Monitering Support Systems"
LABEL version="1.0"

WORKDIR /app

# 모든 파일 복사
COPY . .
# Python 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt