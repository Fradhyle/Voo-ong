# Voo-ong(부엉)
더조은컴퓨터아카데미 빅데이터 10기 최종 팀 프로젝트
---
## 개발 목적
- 영화에 대하여 더욱 세밀한 정보(음악 감독, 미술 감독 등)를 활용하여 더욱 정확한 개인화 추천을 개발하고자 함
## 주의사항
- 원본 데이터 보존 철저
- 개발 기반 환경 동기화 
## 개발 환경
- 기본 언어: Python ([Miniforge 배포판](https://conda-forge.org/download/)) 최신
- 배포판 최신 버전 유지 필수
- 본인 취향에 맞는 개발 툴 쓰시고, **개발 툴 환경설정 폴더는 커밋하지 마세요.**
## 서버 환경
### 크롤러
#### 구성
- Microsoft Azure Virtual Machine
- Microsoft Azure CentOS-based 7.7
- Python (Miniforge) 최신
### 웹 서버
#### 강사님 권장사항
1. Flask 단독
2. 웹 서버 + Flask(기계 학습 모델)
3. 자바 WAS(ex. Apache Tomcat) + Flask(기계 학습 모델)
#### 우리 프로젝트 구성
- Microsoft Azure Virtual Machine
- Microsoft Azure CentOS-based 7.7
- NGINX 최신
- NodeJS 최신
- 구조
    - NGINX: 웹 프론트(요청 및 응답, Java 및 JavaScript 파일 프록시 처리)
    - NodeJS: JavaScript 처리
### Hadoop 클러스터
#### 구성
- Apache Ambari 또는 Cloudera 활용
### RDB 서버 (MySQL 또는 MariaDB)
#### 구성
- Microsoft Azure Virtual Machine
- Microsoft Azure CentOS-based 7.7
- MySQL 최신
## 참고 자료
### Python Miniforge 배포판
- [conda-forge](https://conda-forge.org/)
- [conda-forge Installer](https://conda-forge.org/download/)
### YUM을 이용한 MySQL 설치
- [MySQL :: A Quick Guide to Using the MySQL Yum Repository](https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/)
### IMDB
- [IMDb](https://imdb.com)
- [IMDb Datasets](https://developer.imdb.com/non-commercial-datasets/)
- [IMDb Datasets 다운로드](https://datasets.imdbws.com/)
### GroupLens (MovieLens)
- [GroupLens](https://grouplens.org/)
- [MovieLens](https://movielens.org/)
- [MovieLens Datasets](https://grouplens.org/datasets/movielens/)
- [MovieLens Latest Datasets](https://grouplens.org/datasets/movielens/latest/)
### The Movie DB
- [The Movie Database (TMDb)](https://www.themoviedb.org/)
### KOBIS
- [영화관 입장권 통합전산망](http://www.kobis.or.kr/)
### KMDb
- [KMDb 한국영화데이터베이스](https://www.kmdb.or.kr/)
### 네이버
- [검색 API 영화 검색 개발가이드](https://developers.naver.com/docs/search/movie/)
### 리뷰 텍스트 분석을 위한 데이터셋 구축 
- [Sentiment Analysis](http://ai.stanford.edu/~amaas/data/sentiment/)
### 영화 추천을 위한 협업 필터링
- [Collaborative Filtering for Movie Recommendations](https://keras.io/examples/structured_data/collaborative_filtering_movielens/)
