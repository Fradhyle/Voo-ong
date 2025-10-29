"""설정 파일 작성 및 읽기와 관련된 작업을 수행하는 모듈입니다.
이 모듈은 Dictionary 형식의 설정 데이터를 JSON으로 저장하고, JSON 파일을 불러와서 Dictionary 형식으로 돌려줍니다."""

import json
from json.decoder import JSONDecodeError
from pathlib import Path


class ConfigManager:
    def __init__(self, config_file=None):
        self.config_file = config_file or "config.json"
        self.config = self.load()

    def load(self):
        """클래스에 선언된 config_file에서 설정을 불러옵니다."""
        with open(file=self.config_file, mode="a+", encoding="utf-8") as f:
            try:
                self.config = json.load(f)
            except JSONDecodeError:
                print("[주의] 설정 파일이 없거나 잘못 되었습니다. 새로 작성합니다.")
            finally:
                return self.config

    def save(self, config):
        """클래스에 선언된 config_file에 설정을 저장합니다."""
        self.config = config
        with open(self.config_file, mode="w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return self

    def rdb_config(self, profile_name, address, port, username, password, database):
        # 기존 설정이 있다면 기존 설정을 같이 불러와서 저장하도록 함
        try:
            rdb_config = self.config["rdb_config"]
        except KeyError:
            rdb_config = {}

        rdb_config[profile_name] = {
            "address": address,
            "port": port,
            "username": username,
            "password": password,
            "database": database,
        }

        self.config["rdb_config"] = rdb_config

        self.save(config=self.config)
        return self

    # 파일 경로 설정 저장 함수
    def save_file_path_setting(self, profile_name, file_path):
        file_path_settings = {}
        try:
            file_path_settings = self.config["file_path_settings"]
        except KeyError:
            pass
        file_path_settings[profile_name] = {"file_path": file_path}
        self.config["file_path_settings"] = file_path_settings
        self.save(config=self.config)
        return self

    # 네이버 영화 크롤링 관련 주소 저장
    def save_naver_movie_path(self, address):
        naver_movie_address = {"naver_movie": address}
        return naver_movie_address

    # User-Agent 정보 저장
    def save_ua_info(self, user_agent):
        headers = {"user-agent": user_agent}
        self.config["headers"] = headers
        self.save(config=self.config)
        return self


# 모듈 직접 실행 방지
if __name__ == "__main__":
    print("이 파일을 직접 실행할 수 없습니다.")
    print("main.py를 실행하세요.")
    raise SystemExit
