FROM oraclelinux:10-slim

ENV JAVA_HOME=/usr/java/latest
ENV PATH=$PATH:$JAVA_HOME/bin

RUN microdnf install -y oraclelinux-release-el10 \
    && microdnf clean all

RUN microdnf install -y \
    python3 \
    python3-pip \
    which \
    wget \
    tar \
    gzip \
    procps \
    hostname \
    findutils \
    && microdnf clean all