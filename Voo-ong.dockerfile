FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    locales \
    tzdata \
    python3 \
    python3-pip \
    python3-venv \
    default-jdk \
    && localedef -i ko_KR -c -f UTF-8 -A /usr/share/locale/locale.alias ko_KR.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR:ko
ENV LC_ALL ko_KR.UTF-8
ENV TZ=Asia/Seoul

RUN ln -s /usr/bin/python3 /usr/bin/python \
    && rm -f /usr/lib/python3.*/EXTERNALLY-MANAGED

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

RUN python --version && java -version