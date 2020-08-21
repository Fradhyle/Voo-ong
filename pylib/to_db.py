# to_db.py

# 프로그램 시작 파일 설정
if __name__ == '__main__':
    import os
    os.chdir('..')
    import main
    main.menu()

from sqlalchemy import create_engine
import sqlalchemy
import math


def create_table(settings, table_name, df):
    rdb_settings = {}
    try:
        rdb_settings = settings['rdb_settings']
    except KeyError:
        print('RDB 서버 설정을 찾을 수 없습니다. RDB 서버 설정 후 다시 시도하세요.')
        import main
        main.menu()
    choice = 0
    while True:
        try:
            print('어떤 프로필을 사용하여 접속하시겠습니까?')
            i = 1
            for key in rdb_settings.keys():
                print(str(i) + '. ' + key)
                i += 1
            choice = int(input('>>> ')) - 1
        except TypeError:
            print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
            continue
        except ValueError:
            print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
            continue
        else:
            break
    selected_key = list(rdb_settings.keys())[choice]
    address = rdb_settings[selected_key]['address']
    port = rdb_settings[selected_key]['port']
    username = rdb_settings[selected_key]['username']
    password = rdb_settings[selected_key]['password']
    database = rdb_settings[selected_key]['database']
    print()
    print('선택한 프로필의 정보입니다.')
    print()
    print('서버 주소 및 포트:', address + ':' + port)
    print('사용자명:', username)
    print('비밀번호:', password)
    print('데이터베이스명:', database)
    print()
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
            print('RDB 적재 작업을 시작합니다.')
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
    _columns = df.columns
    max_length = {}
    dtypes = {}
    try:
        from langdetect import detect
    except ModuleNotFoundError:
        print('필요한 모듈이 발견되지 않아서 설치를 수행합니다.')
        import os
        os.system('pip install langdetect')
    import numpy as np
    for _ in _columns:
        print(f'컬럼명 {_}에 대한 연산을 수행중입니다.')
        dtypes[_] = sqlalchemy.types.TEXT()
        # try:
        #     lang = df[_].apply(str).apply(detect)
        # except:
        #     lang = np.nan
        # if [lang == 'ko']:
        #     max_length[_] = max(df[_].apply(str).apply(len)) * 2
        # max_length[_] = max(df[_].apply(str).apply(len))
        # if max_length[_] > 5000:
        #     dtypes[_] = sqlalchemy.types.TEXT()
        # else:
        #     value_length = math.ceil(max_length[_] * 1.1)
        #     dtypes[_] = sqlalchemy.types.String(length=value_length)
    print(dtypes)
    sql_engine = create_engine(f'mysql+pymysql://{username}:{password}@{address}:{port}/{database}'
                               f'?charset=utf8mb4', encoding='utf-8', echo=True)
    db_conn = sql_engine.connect()
    t_method = ''
    while True:
        try:
            # 선택 내용 확인
            print()
            print('같은 이름의 테이블이 존재할 경우 어떻게 처리하시겠습니까?\n'
                  '1. 적재 작업 중단\n'
                  '2. 테이블 대체\n'
                  '3. 로우 추가')
            choice = int(input('>>> '))
        except TypeError:
            print('잘못 입력하였습니다. 다시 입력하세요.')
            continue
        except ValueError:
            print('잘못 입력하였습니다. 다시 입력하세요.')
            continue
        if choice == 1:
            t_method = 'fail'
            break
        elif choice == 2:
            t_method = 'replace'
            break
        elif choice == 3:
            t_method = 'append'
            break
        else:
            print('잘못 선택하였습니다. 다시 시도하세요.')
            continue
    try:
        print('RDB에 적재를 시작합니다.')
        df.to_sql(table_name, db_conn, if_exists=t_method, index=False, dtype=dtypes, chunksize=500)
    except ValueError as vx:
        print(vx)
        print('오류가 발생하여 처리되지 않았습니다.')
    except Exception as ex:
        print(ex)
        print('오류가 발생하여 처리되지 않았습니다.')
    else:
        print(f'{table_name} 테이블이 정상적으로 처리되었습니다.')
    finally:
        db_conn.close()
        print('메인 메뉴로 돌아갑니다.')
        import main
        main.menu()
