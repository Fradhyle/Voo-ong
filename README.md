# 🎬 Voo-ong (부엉) - 빅데이터·머신러닝 기반 개인화 영화 추천 시스템

[![Portfolio Website](https://img.shields.io/badge/Portfolio_Deck-GitHub_Pages-2563eb?style=for-the-badge&logo=github)](https://Fradhyle.github.io/Voo-ong)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Apache Hadoop](https://img.shields.io/badge/Apache_Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black)](#)
[![Apache Hive](https://img.shields.io/badge/Apache_Hive-FDEE21?style=for-the-badge&logo=apachehive&logoColor=black)](#)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](#)
[![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)](#)

> **타인의 리뷰 편향을 배제한 2,800만 건의 이용자 평점 데이터와 영화 제작진(Crew)·다중 장르 메타데이터를 결합한 개인 맞춤 영화 추천 시스템**  
> 📊 **상세 아키텍처 및 프레젠테이션 포트폴리오:** **[https://Fradhyle.github.io/Voo-ong](https://Fradhyle.github.io/Voo-ong)**

---

## 📌 프로젝트 히스토리 및 아카이빙 안내 (Project Status & Refactoring Note)

본 리포지토리는 **2020년 수행된 빅데이터 팀 프로젝트 원본 산출물**과 이후 개인적으로 진행한 **코드 모듈화(Refactoring) 및 인프라 환경 최신화 내역**을 함께 포함하고 있습니다. 코드를 열람하실 때 아래 타임라인과 외부 환경 변경 사항을 참고해 주시기 바랍니다.

1. **Phase 1 — 최초 프로젝트 구축 및 완수 (2020.03 ~ 2020.06)**
   * **인프라 및 OS:** Microsoft Azure IaaS → Oracle VirtualBox 온프레미스 클러스터 전환 (`CentOS 7.7`, `Cloudera Manager CDH 6.3.1` / `Apache Ambari 2.7.4`)
   * **데이터 및 모델링:** `Anaconda` 배포판 및 **Jupyter Notebook (`.ipynb`)** 환경에서 2,800만 건 데이터 전처리, Hive 적재 및 Keras 다중 레이블 분류 모델(검증 정확도 `86.86%`) 구현 완수
2. **Phase 2 — 사후 코드 리팩토링 및 환경 마이그레이션 (Post-Project Refactoring)**
   * **노트북 코드의 패키지화 (`Apps/pylib/`):** 초기 프로토타이핑 단계에서 `.ipynb` 파일들로 파편화되어 있던 데이터 수집·정제·RDB 적재 스크립트를 재사용 가능한 **CLI 기반 Python 패키지 구조(`config_manager`, `controller`, `crawler`, `file_loader`, `mysql_manager`, `to_db`)** 로 점진적 리팩토링 진행
   * **OS 및 Python 배포판 최신화:** `CentOS 7` 지원 종료(EOL) 및 `Anaconda` 라이선스 정책 변화에 맞추어 기준 서버 환경을 **`Ubuntu (Latest)`** 로, 패키지 관리 환경을 **`Miniforge (conda-forge)`** 로 전환
3. **⚠️ 외부 크롤링 대상 서비스 종료 안내 (`네이버 영화`)**
   * 한국어 영화 제목 및 제작 스태프 수집을 담당하던 `Apps/pylib/crawler.py` 및 관련 노트북은 구 **네이버 영화(`movie.naver.com`)** 의 고유 영화 코드 및 HTML DOM 구조를 기반으로 설계되었습니다.
   * 이후 **네이버 영화 웹사이트가 공식 폐쇄(통합 검색 개편)** 됨에 따라 현재 해당 URL로의 실시간 크롤링은 동작하지 않으며, 멀티스레딩(`ThreadPoolExecutor`) 및 실패 코드 자동 재시도(Retry) 설계를 보여주는 **엔지니어링 아카이브 목적**으로 보존되어 있습니다.

---

## 🎯 기획 의도 및 핵심 해결 과제

* **기존 추천 시스템의 한계:** 대중적인 흥행작이나 타인의 리뷰·평점에 영향을 받아 이용자 고유의 취향이 희석되며, 주연 배우나 유명 감독 위주로만 추천이 이루어져 촬영·음악·무술 감독 등 영화의 분위기('결')를 좌우하는 세부 제작진 및 복합 장르 특성이 누락됨
* **Voo-ong의 해결 방안:**
  1. **개인 평점 정규화(`MinMaxScaler`) 및 `4:2:4` 감성 구간화:** 타인의 리뷰를 배제하고 개인의 평점 분포를 긍정(`+1`), 중립(`0`), 부정(`-1`)으로 변환하여 개인별 19개 장르 선호도 가중치 매트릭스(`ratings_genres`) 산출
  2. **3대 이기종 영화 DB 스키마 통합:** 글로벌 데이터셋(**MovieLens** 2,800만 건 평점·태그 게놈, **IMDb** 영화·인물·직군)과 한국어 서비스용 **네이버 영화** 데이터를 수집하여 37개 표준 장르 매핑 테이블(`voo_ong.genres`)로 통합
  3. **다중 레이블 딥러닝 분류(Multi-Label Classification):** 2,275만 건의 선호 영화 데이터를 기반으로 이용자가 선호할 복합 장르 조합을 예측하는 신경망 모델 구축 및 옵티마이저(`SGD`, `Adam`, `Nadam`) 비교 검증

---

## 🛠️ 시스템 환경 비교 (2020 최초 구축 vs 사후 리팩토링)

| 구분 | 2020 최초 프로젝트 수행 환경 (PPT 발표자료 기준) | 사후 리팩토링 및 최신화 환경 (`Apps/` 기준) |
| :--- | :--- | :--- |
| **OS / Infra** | Microsoft Azure VM → VirtualBox (`CentOS 7.7`, 16GB RAM, 4 vCPU) | `Ubuntu Latest` (CentOS 7 EOL 대응 마이그레이션) |
| **Big Data DW** | `Apache Hadoop (HDFS)`, `Apache Hive`, `Apache Sqoop`, `Hue` (`Cloudera CDH 6.3.1` / `Ambari 2.7.4`) | 좌동 (`PyHive` 및 `SQLAlchemy` 연동 유지) |
| **RDBMS / Web** | `MySQL 8 Community Server` (`utf8mb4`), `NGINX` (Reverse Proxy) + `Node.js v14` | `MySQL` / `MariaDB` 다중 프로필 JSON 설정 구조 |
| **Python 환경** | `Anaconda Individual Edition` (Python 3.7) | `Miniforge` (`conda-forge` 채널 기반 `environment.yml`) |
| **코드 아키텍처** | 단계별 **Jupyter Notebook (`.ipynb`)** 스크립트 중심 | 기능별 분리된 **Python CLI 패키지 (`Apps/pylib/`)** |

---

### 💡 웹 서버 아키텍처 독자 설계 배경 (기존 가이드라인 vs 자체 구축 구성)

교육 과정 당시 제시된 기본 웹 서버 가이드라인을 그대로 따르지 않고, 가용 서버 리소스(VM 사양 제약)와 프론트/백엔드 역할 분리를 고려하여 자체적으로 아키텍처를 재설계했습니다.

* **기존 교육과정 권장 구성안 (미채택)**
  1. `Flask` 단독 서버 구성 (정적/동적 처리 분리 불가 및 동시 요청 처리 한계)
  2. `웹 서버 + Flask(기계 학습 모델)` 구성
  3. `Java WAS(Apache Tomcat 등) + Flask(기계 학습 모델)` 구성 (제한된 VM 사양에서 무거운 WAS 구동 시 리소스 오버헤드 발생)
* **우리 프로젝트의 자체 설계 구성 (`NGINX` + `Node.js`)**
  * **도입 배경:** 클라우드 비용 절감을 위해 낮춘 VM 사양의 한계를 극복하고자, Apache HTTPd나 무거운 WAS 대신 가볍고 비동기 처리에 강한 조합을 독자적으로 채택했습니다.
  * **NGINX (Web Front / Reverse Proxy):** 클라이언트 요청 및 응답 처리, 내부 Java 및 JavaScript(Node.js) 파일 리버스 프록시 라우팅 담당
  * **Node.js (Application Server):** 비동기 이벤트 기반 동적 콘텐츠 및 JavaScript 비즈니스 로직 처리 (`npm`, `Yarn` 패키지 매니저 연동)

---

## 📂 디렉터리 및 주요 파일 구조

```text
Voo-ong/
├── index.html                                        # GitHub Pages 프레젠테이션 포트폴리오
├── Assets/
│   ├── CSS/
│       └── style.css                                 # GitHub Pages를 위한 CSS 파일
│   └── Images/
│       └── Logo.png # Voo-ong 로고 파일
├── Apps/                                             # [사후 리팩토링] CLI 기반 데이터 수집·RDB 적재 Python 패키지
│   ├── main.py                                       # 대화형 CLI 메인 메뉴 진입점
│   └── pylib/
│       ├── config_manager.py                         # RDB 프로필·파일 경로·User-Agent 헤더 JSON 설정 관리
│       ├── controller.py                             # 사용자 입력 검증 및 크롤링·적재 실행 제어
│       ├── crawler.py                                # ThreadPoolExecutor 멀티스레드 크롤러 (최대 5회 자동 재시도 및 난수 대기)
│       ├── file_loader.py                            # 대용량 CSV 로드 및 Pandas DataFrame 변환 (FileToDF)
│       ├── mysql_manager.py / mysql_ctrl.py          # MySQL Connector/Python 기반 커넥션 및 쿼리 실행 관리
│       ├── to_db.py                                  # SQLAlchemy(mysql+pymysql) 기반 테이블 생성 및 일괄 적재
│       └── create_imdb_movie_table.py                # IMDb 다중 장르 파싱 및 정규화 적재
├── Hive QL/                                          # Hadoop Hive 데이터 웨어하우스 DDL/DML 스크립트
│   ├── CREATE DATABASE movielens.hql                 # MovieLens 평점·영화·태그·게놈 테이블 스키마 정의
│   ├── imdb CREATE DATABASE, CREATE TABLE.hql        # IMDb 인물·직군·영화·크루 스키마 정의
│   ├── naver_movie CREATE DATABASE, CREATE TABLE.hql # 네이버 영화·배우·스태프·직군 스키마 정의
│   ├── INSERT INTO voo_ong.genres.hql                # IMDb·MovieLens·네이버 영화 37개 표준 장르 통합 매핑
│   └── INSERT INTO mlens.*.hql                       # 장르 원-핫 인코딩 및 평점 스케일링 테이블 생성
├── 이용자별 장르 평점 계산/                            # 2,800만 건 평점 기반 개인별 19개 장르 선호도 집계 모듈
│   ├── main.py / aggregation.py                      # PyHive 연동 및 긍정(+1)/부정(-1) 장르 가중치 합산 배치 코드
├── Multi Label Classification.ipynb                  # Keras 다중 레이블 분류 모델 학습 및 SGD·Adam·Nadam 비교 실험
├── MovieLens *.ipynb / IMDb *.ipynb                  # [2020 원본] 데이터 전처리·원핫 인코딩·적재 주피터 노트북
└── 발표 자료/                                         # 프로젝트 발표용 PPTX 및 208페이지 전체 구축 매뉴얼 PPTX
```

---

## 📊 딥러닝 모델링 및 실험 결과 요약

* **학습 데이터 규모:** 원천 평점 **2,800만 건** 중 부정 평가를 제외한 **2,275만 건** (Train **17,069,567건** / Validation **5,689,856건**)
* **신경망 구조:** `Input(19개 장르 선호도)` → `Dense(5000, ReLU)` → `Dropout(0.1)` → `Dense(600, ReLU)` → `Dropout(0.1)` → `Dense(Output, Sigmoid)`
* **손실 함수 및 배치 설정:** `binary_crossentropy`, `batch_size = 5000`, `epochs = 10`, `workers = 80 (multiprocessing)`

| Optimizer | 세부 하이퍼파라미터 | 훈련 정확도 (Train Acc) | 검증 정확도 (Val Acc) | 검증 손실률 (Val Loss) |
| :--- | :--- | :---: | :---: | :---: |
| **SGD** | `lr=0.01, momentum=0.9, decay=1e-6, nesterov=True` | 0.8683 | 0.8685 | 0.3168 |
| **Adam (Best)** | Adaptive Moment Estimation (Default) | **0.8685** | **0.8686** (최고 0.8687) | **0.3154** |
| **Nadam** | Adam + Nesterov Momentum | 0.8684 | 0.8685 | 0.3159 |

---

## 🔗 참고 자료 및 데이터 출처 (References)

* **Datasets:** [GroupLens MovieLens Datasets](https://grouplens.org/datasets/movielens/) / [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/) / [KMDb](https://www.kmdb.or.kr/) / [KOBIS](http://www.kobis.or.kr/)
* **Environment & DB:** [Miniforge (conda-forge)](https://conda-forge.org/download/) / [MySQL Yum Repository Guide](https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/) / [Cloudera Documentation](https://docs.cloudera.com/documentation/enterprise/latest/topics/introduction.html)
* **Algorithm & Papers:** [Keras Collaborative Filtering for Movie Recommendations](https://keras.io/examples/structured_data/collaborative_filtering_movielens/) / [Scalable Realistic Recommendation Datasets through Fractal Expansions (arXiv:1901.08910)](https://arxiv.org/abs/1901.08910)
