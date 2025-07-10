FROM python:3.11-slim

WORKDIR /

# 시스템 패키지 설치 (MySQL 드라이버 등 필요시)
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 소스 코드 복사
COPY . .

# FastAPI 기본 포트
EXPOSE 8080

# 기본 실행 명령 (uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]