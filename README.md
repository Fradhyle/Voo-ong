# Voo-ong(부엉)
더조은컴퓨터아카데미 빅데이터 10기 최종 팀 프로젝트
---
- ## 주의사항
    - ### 원본 데이터 보존 철저
    - ### 환경 동기화 
1. 개발 환경
    - 기본 언어: Python (Anaconda) 최신
        - Anaconda 최신 버전 유지 필수
            - Anaconda 관리자 모드로 실행 후 ```conda update --all``` 수행
    - 본인 취향에 맞는 개발 툴 쓰시고, **개발 툴 환경설정 폴더는 커밋하지 마세요.**
2. 서버 환경
    - 크롤러
        - 구성
            - Microsoft Azure Virtual Machine
            - Microsoft Azure CentOS-based 7.7
            - Python (Anaconda) 최신
    - 웹 서버
        - 강사님 권장사항
            1. Flask 단독
            2. 웹 서버 + Flask(기계 학습 모델)
            3. 자바 WAS(ex. Apache Tomcat) + Flask(기계 학습 모델)
        - 구성
            - Microsoft Azure Virtual Machine
            - Microsoft Azure CentOS-based 7.7
            - NGINX 최신
            - NodeJS 최신
        - 구조
            - NGINX: 웹 프론트(요청 및 응답, Java 및 JavaScript 파일 프록시 처리)
            - NodeJS: Java 및 JavaScript 처리
    - 하둡 클러스터
        - 구성
            - Apache Ambari 활용
    - RDB 서버
        - 구성
            - Microsoft Azure Virtual Machine
            - Microsoft Azure CentOS-based 7.7
            - MySQL 최신
3. 참고 자료
    - YUM을 이용한 MySQL 설치
        - [MySQL :: A Quick Guide to Using the MySQL Yum Repository](https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/)
    - IMDB
        - [IMDb](https://imdb.com)
        - [IMDb Datasets](https://www.imdb.com/interfaces/)
        - [IMDb Datasets 다운로드](https://datasets.imdbws.com/)
    - GroupLens (MovieLens)
        - [GroupLens](https://grouplens.org/)
        - [MovieLens](https://movielens.org/)
        - [MovieLens Datasets](https://grouplens.org/datasets/movielens/)
    - The Movie DB
        - [The Movie Database (TMDb)](https://www.themoviedb.org/)
    - KOBIS
        - [영화관 입장권 통합전산망](http://www.kobis.or.kr/)
    - KMDb
        - [KMDb 한국영화데이터베이스](https://www.kmdb.or.kr/)
    - 네이버
        - [검색 API 영화 검색 개발가이드](https://developers.naver.com/docs/search/movie/)
    - 리뷰 텍스트 분석을 위한 데이터셋 구축 
        - [Sentiment Analysis](http://ai.stanford.edu/~amaas/data/sentiment/)
