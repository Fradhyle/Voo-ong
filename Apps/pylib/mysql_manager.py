import json
from pathlib import Path

import mysql.connector
from mysql.connector import Error


class MySQLManager:
    """MySQL과의 연결 및 쿼리 실행을 관리하는 클래스"""

    def __init__(self, config_path: Path = None):
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "db_config.json"
            config_path = config_path.absolute()

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.connection = None

    def connect(self):
        """MySQL 연결 생성"""
        if self.connection and self.connection.is_connected():
            return self.connection

        try:
            self.connection = mysql.connector.connect(**self.config)
            print(
                f"MySQL 연결 성공: {self.config['host']}:{self.config['port']}:{self.config['database']}"
            )
        except Error as e:
            print(f"MySQL 연결 실패: {e}")
            self.connection = None

        return self.connection

    def execute_query(self, query: str, params: tuple = None, commit: bool = False):
        """쿼리 실행"""
        cnx = self.connect()
        if not cnx:
            raise ConnectionError("MySQL 서버에 연결할 수 없습니다.")

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if commit:
                cnx.commit()
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result
            return None
        except Error as e:
            print(f"쿼리 실행 실패: {e}")
        finally:
            cursor.close()

    def close(self):
        """MySQL 연결 종료"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL 연결 종료")
