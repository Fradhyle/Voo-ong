# settings_manager.py
# 이 프로그램과 관련된 설정을 Dictionary 형식으로 저장하는 모듈

# 프로그램 시작 파일 설정
if __name__ == '__main__':
    import os
    os.chdir('..')
    import main
    main.menu()

from pylib.json_manager import JsonManager

jm = JsonManager()
settings = {}


class SettingsManager:
    def __init__(self):
        self.settings = jm.json_load()

    # RDB 설정 저장 함수
    def save_rdb_setting(self, profile_name, address, port, username, password, database):
        rdb_settings = {}
        try:
            rdb_settings = self.settings['rdb_settings']
        except KeyError:
            pass
        rdb_settings[profile_name] = {'address': address, 'port': port, 'username': username,
                                      'password': password, 'database': database}
        self.settings['rdb_settings'] = rdb_settings
        jm.json_save(settings=self.settings)
        return self

    # 파일 경로 설정 저장 함수
    def save_file_path_setting(self, profile_name, file_path):
        file_path_settings = {}
        try:
            file_path_settings = self.settings['file_path_settings']
        except KeyError:
            pass
        file_path_settings[profile_name] = {'file_path': file_path}
        self.settings['file_path_settings'] = file_path_settings
        jm.json_save(settings=self.settings)
        return self

    # 네이버 영화 크롤링 관련 주소 저장
    def save_naver_movie_path(self, address):
        naver_movie_address = {'naver_movie': address}
        return naver_movie_address

    # User-Agent 정보 저장
    def save_ua_info(self, user_agent):
        iheaders = {'user-agent': user_agent}
        self.settings['iheaders'] = iheaders
        jm.json_save(settings=self.settings)
        return self
