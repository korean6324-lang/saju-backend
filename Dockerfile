# Dockerfile
# Python 3.11 경량화 버전을 베이스 이미지로 사용
FROM python:3.11-slim

# 환경 변수 설정 (파이썬 출력 버퍼링 제거 및 바이트코드 생성 방지)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Seoul

# 컨테이너 내 작업 디렉토리 생성
WORKDIR /app

# 시스템 의존성 패키지 설치 (시간대 설정용)
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get clean

# 파이썬 라이브러리 설치 (ephem, fastapi, redis 등)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Phase 1 ~ Track B까지 개발된 모든 소스코드 복사
COPY . /app/

# 외부로 노출할 포트
EXPOSE 8000

# FastAPI 서버 실행 (운영 환경용 Uvicorn 워커 구동)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]