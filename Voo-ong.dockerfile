# 2026년 03월 31일 기준 Python의 최신 안정 버전의 가벼운 이미지를 이용하도록 설정
FROM python:3.14-slim

# Python 환경변수를 설정하여 바이트코드 생성과 출력 버퍼를 제거
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 시간대 및 언어 설정
ENV TZ=Asia/Seoul
ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR:ko
ENV LC_ALL=ko_KR.UTF-8

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    tzdata

# 시스템 시간대 및 로케일 적용
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && sed -i '/ko_KR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen ko_KR.UTF-8 \
    && update-locale LANG=ko_KR.UTF-8 LC_ALL=ko_KR.UTF-8

# 프로그램 실행에 필요한 런타임 시스템 라이브러리 설치 (PostgreSQL, Hive 관련)
RUN apt-get install -y --no-install-recommends \
    libpq5 \
    libsasl2-2

# 7. 파이썬 패키지 설치 및 최적화
# 주의: 빌드 도구를 설치하고 패키지를 컴파일한 뒤 바로 삭제해야 도커 이미지 용량이 줄어들기 때문에 하나의 RUN으로 묶여 있습니다.
RUN apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libsasl2-dev \
    # pip 도구 최신화
    && pip install --no-cache-dir --upgrade pip \
    # 데이터 수집, 정제, 적재에 필요한 공식 및 필수 라이브러리 설치
    && pip install --no-cache-dir \
    psycopg2 \
    sqlalchemy \
    pandas \
    numpy \
    beautifulsoup4 \
    aiohttp \
    tqdm \
    pyarrow \
    pyhive[hive] \
    thrift \
    sasl \
    thrift_sasl \
    # 설치가 완료되면 컴파일에만 사용되었던 빌드 도구 삭제 (이미지 경량화)
    && apt-get purge -y --auto-remove \
    build-essential \
    libpq-dev \
    libsasl2-dev \
    # apt 캐시 정리
    && rm -rf /var/lib/apt/lists/*

# 8. 작업 디렉토리 설정 (컨테이너 내부 기준)
WORKDIR /app

# 9. 로컬의 소스 코드를 컨테이너 내부로 복사
COPY . /app

# 10. 컨테이너 실행 시 기본으로 수행할 실행 명령어 지정
CMD ["python", "main.py"]