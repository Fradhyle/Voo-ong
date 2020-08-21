# json_manager.py

# 프로그램 시작 파일 설정
if __name__ == '__main__':
    import os
    os.chdir('..')
    import main
    main.menu()

# JSON 모듈이 빈 파일을 불러올 때 발생하는 오류 처리 import
from json.decoder import JSONDecodeError
# 파일을 JSON 포맷으로 저장하는 json 모듈 import
import json


# JSON 파일 관리 클래스
class JsonManager:
    # 클래스 멤버 변수 선언
    def __init__(self):
        # JSON 파일 객체를 저장하는 변수
        self.json_data = ''
        # 프로그램의 설정이 저장된 Dictionary를 저장하는 변수
        self.settings = {}
        # 설정 파일의 이름을 저장하는 변수
        self.settings_file = ''

    # JSON 파일 불러오기 함수
    def json_load(self, settings_file='settings.json'):
        # JSON 파일 불러오기
        try:
            self.json_data = open(settings_file, 'r', encoding='utf-8')
        # 기존 JSON 파일이 존재하지 않는 경우 JSON 파일 생성 후 다시 불러오기
        except FileNotFoundError:
            print('설정 파일이 발견되지 않았습니다. 설정 파일을 새로 작성합니다.')
            self.json_data = open(settings_file, 'w', encoding='utf-8')
            self.json_data = open(settings_file, 'r', encoding='utf-8')
        # JSON 파일에서 데이터 불러오기
        try:
            self.settings = json.load(self.json_data)
        # JSON 데이터를 불러올 때 발생할 수 있는 오류 처리. 예: 빈 파일
        except JSONDecodeError:
            pass
        # 불러온 설정값 반환
        finally:
            return self.settings

    # JSON 파일 저장 함수
    def json_save(self, settings, settings_file='settings.json'):
        # 설정이 저장된 Dictionary를 클래스 내 멤버 변수에 대입
        self.settings = settings
        # 설정 저장 파일 열기
        self.settings_file = open(settings_file, 'w', encoding='utf-8')
        # 설정이 저장된 Dictionary를 JSON 형태로 변환
        self.json_data = json.dumps(self.settings, ensure_ascii=False, indent=4, separators=(',', ':'))
        # 파일 작성
        self.settings_file.write(self.json_data)
        # 파일 닫기
        self.settings_file.close()
