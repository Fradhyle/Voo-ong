"""MovieLens 영화 장르 테이블 만들기
이 모듈은 MovieLens의 데이터셋에 있는 영화 장르 이름을 추출하여 DB 테이블을 생성합니다."""

# MySQL Connector 모듈 및 pandas 모듈 import
import mysql.connector as mqc
import pandas as pd

# MySQL 연결 객체 생성
cnx = mqc.connect(
    host="v.pdmnu.com",
    user="root",
    password="!Bigdata10",
    database="mlens",
)

# MySQL 동작을 실질적으로 실행하는 cursor 객체 생성
cursor = cnx.cursor()

# 실행할 쿼리문 입력
query = "SELECT genres FROM mlens.movies;"

# cursor 객체를 통하여 쿼리 실행
cursor.execute(query)

# 결과물을 저장할 리스트 선언
genres = []

# 결과물을 리스트에 저장
# 한 개의 컬럼만 조회하였지만 결과물이 튜플들의 리스트로 반환되기 때문에 0번째 인덱스의 값만 가져오도록 코드 작성
for _ in cursor:
    genres.append(_[0])

# 결과물을 저장할 Series 객체 생성
genres_series = pd.Series(genres)

# 가져온 내용을 |(수직선)을 기준으로 분할하여 DataFrame으로 저장
genres_split = genres_series.str.split("|", expand=True)

genres_series = pd.Series()

for _ in range(len(genres_split.columns)):
    # 겹치는 이름을 삭제하기 위하여 모든 컬럼을 하나의 Series 객체로 합침
    genres_series = pd.concat([genres_series, genres_split[_]])

# unique() 메서드를 활용하여 중복값을 제거한 후 반환된 ndarray 객체를 다시 Series 객체로 생성
# 이후 값을 기준으로 재정렬
genres_series = pd.Series(genres_series.unique(), name="Genres")
genres_series.sort_values(inplace=True, ignore_index=True)

# 정리된 Series 객체의 값만 추출하여 MySQL 쿼리에 대입할 수 있도록 튜플들의 리스트로 변환
value_params = list(
    zip(
        genres_series.T.values,
    )
)

# MySQL 쿼리 실행
query = "INSERT INTO genres (genre_name) VALUES (%s)"
try:
    cursor.executemany(query, value_params)
except mqc.Error as err:
    print("오류가 발생하였습니다:", err)
finally:
    print(str(cursor.rowcount) + "개의 행이 처리되었습니다.")
    cnx.commit()

# MySQL 연결 닫기
cnx.close()
