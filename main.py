# main.py

from pylib.json_manager import JsonManager
import pylib.controller as ctrl


# 메인 메뉴 함수
def menu():
    # JsonManager 클래스 호출
    jm = JsonManager()
    # JSON 파일에서 설정 불러오기
    settings = jm.json_load()
    # 메뉴에 출력될 텍스트
    menu_text = ('=============================\n'
                 '  파일 -> RDB 적재 프로그램\n'
                 '=============================\n'
                 '1. RDB 서버 설정\n'
                 '2. 파일 경로 설정\n'
                 '3. 크롤러 헤더 설정\n'
                 '4. 현재 설정 확인\n'
                 '5. 적재 작업 시작\n'
                 '6. 크롤링 작업 선택\n'
                 '7. 종료')
    # 메뉴 선택
    # 올바른 메뉴를 선택하거나 종료할 때까지 종료되지 않게 함
    while True:
        # 메뉴 텍스트 출력
        print(menu_text)
        # 잘못된 값을 입력한 경우에 대한 오류 처리
        try:
            print()
            choice = int(input('메뉴를 선택하세요: '))
        except TypeError:
            print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
            continue
        except ValueError:
            print('잘못된 값을 입력하였습니다. 다시 시도하세요.')
            continue
        # RDB 서버 설정
        if choice == 1:
            ctrl.set_rdb()
            settings = jm.json_load()
            try:
                settings['rdb_settings']
            except KeyError:
                print('설정이 저장되지 않았습니다. 다시 시도하세요.')
            else:
                print('설정을 저장하였습니다.')
                print()
        # 파일 경로 설정
        elif choice == 2:
            ctrl.set_file_path()
            settings = jm.json_load()
            try:
                settings['file_path_settings']
            except KeyError:
                print('설정이 저장되지 않았습니다. 다시 시도하세요.')
            else:
                print('설정을 저장하였습니다.')
                print()
        # 크롤러 헤더 설정
        elif choice == 3:
            ctrl.set_user_agent()
            settings = jm.json_load()
            try:
                settings['iheaders']
            except KeyError:
                print('설정이 저장되지 않았습니다. 다시 시도하세요.')
            else:
                print('설정을 저장하였습니다.')
                print()
        # 현재 설정 확인
        elif choice == 4:
            ctrl.show_settings(settings)
        # 적재 작업 시작
        elif choice == 5:
            ctrl.start_loading(settings)
        elif choice == 6:
            ctrl.crawl_select(settings)
        # 종료
        elif choice == 7:
            print()
            print('프로그램을 종료합니다.')
            exit()
        # 없는 메뉴 숫자를 입력한 경우
        else:
            print('잘못 선택하였습니다. 다시 시도하세요.')
            continue


# 메인 메뉴 실행
menu()
