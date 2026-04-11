FROM python:3.14-slim

# 환경 변수 (바이트코드 방지, 버퍼링 제거, KST 시간대, UTF-8 로케일)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR:ko \
    LC_ALL=ko_KR.UTF-8

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치, 로케일/시간대 설정, 파이썬 패키지 설치 및 빌드 도구 제거 (단일 RUN으로 압축하여 이미지 경량화)
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    tzdata \
    libpq5 \
    libsasl2-2 \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && sed -i '/ko_KR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen ko_KR.UTF-8 \
    && update-locale LANG=ko_KR.UTF-8 LC_ALL=ko_KR.UTF-8 \
    # 임시 빌드 도구 설치
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libsasl2-dev \
    # pip 최신화 및 필수 라이브러리 설치 (beautifulsoup4, pyarrow 제외)
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    psycopg2 \
    sqlalchemy \
    pandas \
    numpy \
    aiohttp \
    tqdm \
    pyhive[hive] \
    thrift \
    sasl \
    thrift_sasl \
    # 빌드 도구 삭제 및 캐시 정리
    && apt-get purge -y --auto-remove \
    build-essential \
    libpq-dev \
    libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*

# 소스 코드 복사
COPY . /app

# 크롤러 실행 명령어 (실제 실행 파일명으로 수정)
CMD ["python", "main.py"]