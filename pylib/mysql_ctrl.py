# mysql_ctrl.py
# MySQL에서 제공하는 MySQL Connector/Python을 이용하여 MySQL 작업을 실행할 수 있는 모듈

try:
    from mysql.connector import errorcode
    import mysql.connector
except ModuleNotFoundError:
    print('MySQL Connector/Python이 설치되지 않았습니다.')
    print('설치를 시도합니다.')
    import os
    os.system('pip install mysql-connector-python')
finally:
    from mysql.connector import errorcode
    import mysql.connector

# 프로그램 시작 파일 설정
if __name__ == '__main__':
    import os
    os.chdir('..')
    import main
    main.menu()


class MySqlConn:
    def __init__(self):
        from pylib.json_manager import JsonManager
        jm = JsonManager()
        self.settings = jm.json_load()
        self.rdb_settings = self.settings['rdb_settings']
        self.cnx = None

    def conn(self):
        choice = 0
        while True:
            try:
                print('어떤 프로필을 사용하여 접속하시겠습니까?')
                i = 1
                for key in self.rdb_settings.keys():
                    print(str(i) + '. ' + key)
                    i += 1
                choice = int(input('>>> ')) - 1
            except TypeError:
                print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
                continue
            except ValueError:
                print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
                continue
        selected_key = list(self.rdb_settings.keys())[choice]
        address = self.rdb_settings[selected_key]['address']
        port = self.rdb_settings[selected_key]['port']
        username = self.rdb_settings[selected_key]['username']
        password = self.rdb_settings[selected_key]['password']
        database = self.rdb_settings[selected_key]['database']
        print()
        print('선택한 프로필의 정보입니다.')
        print()
        print('서버 주소 및 포트:', address + ':' + port)
        print('사용자명:', username)
        print('비밀번호:', password)
        print('데이터베이스명:', database)
        while True:
            try:
                print('이 프로필이 맞습니까?\n'
                      '1. 예\n'
                      '2. 아니오')
                choice = int(input('>>> '))
            except TypeError:
                print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
                continue
            except ValueError:
                print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
                continue
            if choice == 1:
                break
            elif choice == 2:
                print('처음부터 다시 시작하시기 바랍니다.')
                print('메인 메뉴로 돌아갑니다.')
                import os
                os.chdir('..')
                import main
                main.menu()
            else:
                print('잘못 선택하였습니다. 다시 시도하세요.')
                continue
        try:
            self.cnx = mysql.connector.connect(host=address, port=port, user=username, password=password,
                                               database=database, charset='utf8mb4', autocommit=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('접근이 허가되지 않았습니다. 사용자명 또는 비밀번호가 틀렸을 수 있습니다.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('존재하지 않는 데이터베이스입니다.')
            else:
                print(err)
        else:
            return self.cnx

    def cnx_close(self):
        self.cnx.commit()
        self.cnx.close()
        try:
            self.cnx.ping()
        except self.cnx.InterfaceError:
            return 0

    def insert(self, table_name, **kwargs):
        cursor = self.cnx.cursor()
        values = tuple(kwargs.values())
        table_name = '`' + table_name + '`'
        insert_part = f'INSERT INTO {table_name} ('
        counter = 1
        for _ in kwargs.keys():
            if counter != len(kwargs.keys()):
                insert_part = insert_part + _ + ', '
                counter += 1
            elif counter == len(kwargs.keys()):
                insert_part = insert_part + _ + ') '
        values_part = f'VALUES {values}'
        query = insert_part + values_part
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            print('오류가 발생하였습니다:', err)
        finally:
            print(str(cursor.rowcount) + '개 행이 처리되었습니다.')
            self.cnx.commit()
