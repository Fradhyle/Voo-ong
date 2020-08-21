# controller.py

# 프로그램 시작 파일 설정
if __name__ == '__main__':
    import os
    os.chdir('..')
    import main
    main.menu()

from pylib.file_loader import FileToDF
from pylib.settings_manager import SettingsManager
import pylib.to_db as to_db


def set_rdb():
    print()
    print('RDB 서버 설정을 시작합니다.')
    print()
    profile_name = input('RDB 서버의 프로필 이름을 입력하세요: ')
    address = input('RDB 서버 주소를 입력하세요: ')
    port = input('RDB 서버 포트를 입력하세요: ')
    username = input('RDB 서버 사용자명을 입력하세요: ')
    password = input('RDB 서버 사용자 비밀번호를 입력하세요: ')
    database = input('RDB 서버에서 사용할 데이터베이스 이름을 입력하세요: ')
    print()
    print('입력하신 정보는 아래와 같습니다.')
    print()
    print('RDB 서버 설정')
    print('프로필 이름: ', profile_name)
    print('서버 주소 및 포트:', address + ':' + port)
    print('사용자명:', username)
    print('비밀번호:', password)
    print('데이터베이스명:', database)
    print()
    while True:
        try:
            print()
            print('위 정보가 맞습니까?\n'
                  '1. 예\n'
                  '2. 아니오')
            choice = int(input('>>> '))
        except TypeError:
            print('잘못된 값을 입력하였습니다. 다시 입력하세요.')
            continue
        except ValueError:
            print('잘못된 값을 입력하였습니다. 다시 입력하세요.')
            continue
        if choice == 1:
            sm = SettingsManager()
            sm.save_rdb_setting(profile_name, address, port, username, password, database)
            return
        elif choice == 2:
            print('설정 저장을 취소하였습니다. 메인 메뉴로 돌아갑니다.')
            print()
            import main
            main.menu()
        else:
            print('잘못 선택하였습니다. 다시 시도하세요.')
            continue


def set_file_path():
    print()
    print('파일 경로 설정을 시작합니다.')
    profile_name = input('파일 경로의 프로필 이름을 입력하세요: ')
    path_input = input('작업할 파일이 있는 경로를 입력하세요: ')
    while True:
        try:
            print()
            print(path_input)
            print('위 경로가 맞습니까?')
            choice = int(input('1. 예\n'
                               '2. 아니오\n'))
        except TypeError:
            print('잘못된 값을 입력하였습니다. 다시 입력하세요.')
            continue
        except ValueError:
            print('잘못된 값을 입력하였습니다. 다시 입력하세요.')
            continue
        if choice == 1:
            import re
            pattern = re.compile('\\$')
            regex_result = pattern.search(path_input)
            if regex_result:
                path = path_input.rstrip('\\')
                file_path = path.replace('\\', '/')
                sm = SettingsManager()
                sm.save_file_path_setting(profile_name, file_path)
                return
            else:
                file_path = path_input.replace('\\', '/')
                file_path = file_path + '/'
                sm = SettingsManager()
                sm.save_file_path_setting(profile_name, file_path)
                return
        elif choice == 2:
            print('설정 저장을 취소하였습니다. 메인 메뉴로 돌아갑니다.\n')
            main.menu()
        else:
            print('잘못 선택하였습니다. 다시 시도하세요.')
            continue


# 현재 설정 출력 함수
def show_settings(settings):
    print()
    print('현재 설정입니다.')
    print()
    try:
        rdb_settings = settings['rdb_settings']
    except KeyError:
        print('RDB 서버 설정이 없습니다.')
        print()
    else:
        print('RDB 서버 설정')
        for key in rdb_settings.keys():
            print('프로필 이름:', key)
            print('서버 주소 및 포트:', rdb_settings[key]['address'] + ':' + rdb_settings[key]['port'])
            print('사용자명:', rdb_settings[key]['username'])
            print('비밀번호:', rdb_settings[key]['password'])
            print('데이터베이스명:', rdb_settings[key]['database'])
            print()
    try:
        file_path_settings = settings['file_path_settings']
    except KeyError:
        print('파일 경로 설정이 없습니다.')
    else:
        print('파일 경로 설정')
        for key in file_path_settings.keys():
            print('프로필 이름:', key)
            print('파일 경로:', file_path_settings[key]['file_path'])
            print()
    finally:
        print()
    try:
        iheaders = settings['iheaders']
    except KeyError:
        print('헤더 설정이 없습니다.')
    else:
        print('헤더 설정')
        print('User agent:', iheaders['user-agent'])
    finally:
        print()


def start_loading(settings):
    print()
    print('적재 작업을 시작합니다.')
    loader = FileToDF(settings=settings)
    while True:
        try:
            print()
            print('파일 확장자를 선택하세요.\n'
                  '1. CSV\n'
                  '2. TSV')
            choice = int(input('>>> '))
        except TypeError:
            print('잘못된 값을 입력하였습니다. 다시 입력하세요.')
            continue
        except ValueError:
            print('잘못된 값을 입력하였습니다. 다시 입력하세요.')
            continue
        if choice == 1:
            table_name, df = loader.csv()
            to_db.create_table(settings=settings, table_name=table_name, df=df)
        elif choice == 2:
            table_name, df = loader.tsv()
            to_db.create_table(settings=settings, table_name=table_name, df=df)
        else:
            print('잘못 선택하였습니다. 다시 시도하세요.')
            continue


# 크롤링에 필요한 User Agent 정보 설정 함수
def set_user_agent():
    print()
    print('크롤링에 사용할 User Agent 정보를 저장합니다.')
    print('잠시 후 열린 브라우저에서 User Agent 정보를 복사하여 입력해주세요.')
    import time
    time.sleep(5)
    import webbrowser
    webbrowser.open('https://www.whatismybrowser.com/detect/what-is-my-user-agent')
    user_agent = input('>>> ')
    sm = SettingsManager()
    iheaders = sm.save_ua_info(user_agent)
    return iheaders


# 크롤링할 정보 선택
def crawl_select(settings):
    try:
        settings['iheaders']
    except KeyError:
        print('헤더 설정을 찾을 수 없습니다. 헤더 설정 후 다시 시도하세요.')
        import main
        main.menu()
    print('어떤 정보를 수집하시겠습니까?\n'
          '1. 영화 기본 정보\n'
          '2. 영화 배우/제작진 정보\n'
          '3. 인물 정보\n'
          '4. 장르 정보')
    while True:
        # 잘못된 값을 입력한 경우에 대한 오류 처리
        try:
            choice = int(input('>>> '))
        except TypeError:
            print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
            continue
        except ValueError:
            print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
            continue
        if choice == 1:
            from pylib.crawler import Crawler
            crawler = Crawler(settings=settings)
            movie_basic_info_df = crawler.thread_executor(getattr(crawler, 'naver_movie_basic_info'))
            to_db.create_table(settings=settings, table_name='movie-basic', df=movie_basic_info_df)
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            from pylib.crawler import Crawler
            crawler = Crawler(settings=settings)
            genre_df = crawler.naver_movie_genre()
            to_db.create_table(settings=settings, table_name='genre', df=genre_df)
        else:
            print('잘못 선택하였습니다. 다시 시도하세요.')
            continue
