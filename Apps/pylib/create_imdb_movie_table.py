# 이 모듈은 IMDb의 영화 데이터를 바탕으로 IMDb가 사용 중인 영화 장르 이름을 추출한 후 RDB에 저장합니다.
import Apps.pylib.mysql_manager

# MySQL 연결 객체 생성
mysql = Apps.pylib.mysql_manager.MySQLManager()
cnx = mysql.connect()

# 실행할 쿼리문 입력
query = "SELECT genres FROM imdb.title_basics;"

# cursor 객체를 통하여 쿼리 실행
result = cnx.execute_query(query)

# 결과물을 저장할 리스트 선언
genres = []

# 결과물을 리스트에 저장
# 한 개의 컬럼만 조회하였지만, 결과물이 튜플들의 리스트로 반환되기 때문에 0번째 인덱스의 값만 가져오도록 코드 작성
for _ in result:
    genres.append(_[0])

# 영화마다 장르가 여러개 입력되어 있는 경우가 있어서, 이것을 모두 분리하여 저장
for i, v in enumerate(genres):
    genres[i] = v.split(",")

# 중복된 장르를 제거하기 위해 set 자료형으로 변환 후 다시 리스트로 변환
genres = list(set(genres))

# SQL 쿼리문으로 작성하여 테이블에 삽입
query = "INSERT INTO genres (genre_name) VALUES (%s);"
for genre in genres:
    query = f"INSERT INTO genres (genre_name) VALUES ({genre});"
    cnx.execute_query(query, commit=True)

# MySQL 연결 닫기
cnx.close()
