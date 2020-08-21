# file_loader.py
# 파일을 pandas.DataFrame 객체로 변환해주는 모듈


# 프로그램 시작 파일 설정
if __name__ == '__main__':
    import os
    os.chdir('..')
    import main
    main.menu()

import os
import pandas as pd
from pandas import errors


# 파일을 pandas.DataFrame 객체로 변환해주는 클래스
class FileToDF:
    # 클래스를 불러올 때 실행할 변수수선언
    # JSON에서 불러온 settings 딕셔너리 입력 필수
    def __init__(self, settings):
        # 받아온 settings 딕셔너리를 멤버 변수에 대입
        self.settings = settings
        # 받아온 settings에서 파일 경로 설정값 검색, 대입
        try:
            self.file_path_settings = self.settings['file_path_settings']
        except KeyError:
            print('RDB 서버 설정을 찾을 수 없습니다. RDB 서버 설정 후 다시 시도하세요.')
            import main
            main.menu()
        choice = 0
        while True:
            try:
                print('어떤 파일 경로 프로필을 사용하시겠습니까?')
                i = 1
                for key in self.file_path_settings.keys():
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
        self.selected_key = list(self.file_path_settings.keys())[choice]
        self.file_path = self.file_path_settings[self.selected_key]['file_path']
        print()
        print('선택한 경로의 정보입니다.')
        print()
        print(self.file_path)
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

    # CSV 파일을 pandas.DataFrame 객체로 변환 후 반환하는 함수
    def csv(self):
        # 설정된 파일 경로의 파일 목록 불러오기
        try:
            pwd_file_list = os.listdir(self.file_path)
        # 파일 경로가 설정되지 않았을 경우 메인 메뉴 복귀
        except KeyError:
            print('파일 경로 설정을 찾을 수 없습니다. 파일 경로 설정 후 다시 시도하세요.')
            import main
            main.menu()
        # 파일 경로가 없을 경우 메인 메뉴 복귀
        except OSError:
            print('파일 경로를 찾을 수 없습니다. 파일 경로 설정이 올바른지 확인해주세요.')
            import main
            main.menu()
        # 오류가 없을 경우 진행
        else:
            print('CSV 파일 변환 작업을 시작합니다.')
            selected_file = ''
            i = 1
            for _ in pwd_file_list:
                print(i, end='. ')
                print(_)
                i += 1
            while True:
                try:
                    choice = int(input('어떤 파일을 작업하시겠습니까? '))
                except TypeError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                except ValueError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                choice -= 1
                try:
                    selected_file = pwd_file_list[choice]
                    break
                except IndexError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
            print('선택된 파일은', selected_file, '입니다.')
            print('파일을 불러오는 중입니다.')
            print()
            # DataFrame 생성
            try:
                df = pd.read_csv(self.file_path + selected_file, sep=',', encoding='utf-8', low_memory=False)
            except errors.ParserError:
                print('오류가 발생하였습니다. 파일을 확인한 후 다시 시도하세요.')
                import main
                main.menu()
            # 파일명으로 RDB 테이블명 생성
            table_name = selected_file.replace('.csv', '').replace('.', '_')
            print('입력 예정 테이블 이름:', table_name)
            # 변환된 DataFrame 앞부분을 출력하여 올바른 파일인지 확인
            print(df.head())
            print()
            while True:
                try:
                    # 선택 내용 확인
                    print('위 내용의 파일이 맞습니까?\n'
                          '1. 예\n'
                          '2. 아니오')
                    choice = int(input('>>> '))
                except TypeError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                except ValueError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                if choice == 1:
                    print()
                    return table_name, df
                elif choice == 2:
                    print('메인 메뉴로 돌아갑니다.\n')
                    import main
                    main.menu()
                else:
                    print('잘못 선택하였습니다. 다시 시도하세요.')
                    continue

    # TSV 파일을 pandas.DataFrame 객체로 변환 후 반환하는 함수
    def tsv(self):
        # 설정된 파일 경로의 파일 목록 불러오기
        try:
            pwd_file_list = os.listdir(self.file_path)
        # 파일 경로가 설정되지 않았을 경우 메인 메뉴 복귀
        except KeyError:
            print('파일 경로 설정을 찾을 수 없습니다. 파일 경로 설정 후 다시 시도하세요.')
            import main
            main.menu()
        # 파일 경로가 없을 경우 메인 메뉴 복귀
        except OSError:
            print('파일 경로를 찾을 수 없습니다. 파일 경로 설정이 올바른지 확인해주세요.')
            import main
            main.menu()
        # 오류가 없을 경우 진행
        else:
            print('TSV 파일 변환 작업을 시작합니다.')
            # 선택한 파일 이름을 저장할 변수 선언
            selected_file = ''
            i = 1
            # 파일 목록 출력
            for _ in pwd_file_list:
                print(i, end='. ')
                print(_)
                i += 1
            while True:
                # 파일 목록에서 파일 선택
                try:
                    choice = int(input('어떤 파일을 작업하시겠습니까? '))
                # 잘못 입력한 경우 오류 처리
                except TypeError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                except ValueError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                # 올바른 인덱스값 선택을 위해 1 빼기
                choice -= 1
                try:
                    selected_file = pwd_file_list[choice]
                    break
                # 인덱스값이 잘못 선택된 경우 (예: 0을 입력한 경우)
                except IndexError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
            # 선택된 파일명 출력
            print('선택된 파일은', selected_file, '입니다.')
            print('파일을 불러오는 중입니다.')
            print()
            # DataFrame 생성
            try:
                df = pd.read_table(self.file_path + selected_file, sep='\t', quoting=3, na_values='\\N',
                                   encoding='utf-8', low_memory=False)
            except errors.ParserError:
                print('오류가 발생하였습니다. 파일을 확인한 후 다시 시도하세요.')
                import main
                main.menu()
            # 파일명으로 RDB 테이블명 생성
            table_name = selected_file.replace('.tsv', '').replace('.', '_')
            print('입력 예정 테이블 이름:', table_name)
            # 변환된 DataFrame 앞부분을 출력하여 올바른 파일인지 확인
            print(df.head())
            print()
            while True:
                try:
                    # 선택 내용 확인
                    print('위 내용의 파일이 맞습니까?\n'
                          '1. 예\n'
                          '2. 아니오')
                    choice = int(input('>>> '))
                except TypeError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                except ValueError:
                    print('잘못 입력하였습니다. 다시 입력하세요.')
                    continue
                if choice == 1:
                    print()
                    return table_name, df
                elif choice == 2:
                    print('작업을 취소하였습니다. 메인 메뉴로 돌아갑니다.\n')
                    import main
                    main.menu()
                else:
                    print('잘못 선택하였습니다. 다시 시도하세요.')
                    continue
