"""네이버 영화를 크롤링하는 모듈입니다."""

import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


class Crawler:
    """멀티쓰레드로 크롤링을 실행하는 클래스입니다."""

    def __init__(self, settings):
        cpu_count = os.cpu_count()
        if cpu_count is int:
            self.max_workers = cpu_count * 5
        else:
            self.max_workers = 8
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        try:
            self.headers = settings["headers"]
        except KeyError:
            self.headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
            }

    def thread_executor(self, func):
        """멀티쓰레드로 크롤링을 실행합니다."""
        # 최종 취합 결과물을 저장할 DataFrame 선언
        result_df = pd.DataFrame()

        # 시작 시간 기록
        start_time = time.time()

        # 조회 시작값 입력
        start_point = int(input("시작 번호를 입력하세요: "))

        # 조회 끝값 입력
        end_point = int(input("끝 번호를 입력하세요: "))

        # range 대입
        search_range = range(start_point, end_point + 1)
        print(f"총 {len(search_range)}개를 크롤링합니다.")

        # 멀티쓰레드 처리를 위한 튜플 대입
        func_args = ((self.headers, page_code) for page_code in search_range)
        result_list = []
        retry_count = 5

        while True:
            tqdm_total = len(search_range)
            tqdm_list = list(tqdm(self.executor.map(func, func_args), total=tqdm_total))

            # 조회 실패한 코드 목록 선언
            failure_list = []

            # 실패한 코드를 저장
            for dict_ in tqdm_list:
                if dict_["status"] == "Fail":
                    failure_list.append(dict_["code"])
                else:
                    result_list.append(dict_)

            # 실패한 코드가 있고 재시도 회수가 남은 경우 재시도
            if failure_list and retry_count != 0:
                func_args = ((self.headers, page_code) for page_code in failure_list)
                search_range = len(failure_list)
                print("실패한 내역이 있어, 조회를 재시도합니다.")
                print(failure_list)
                retry_count -= 1
                continue
            # 실패한 코드가 있고 재시도 회수가 없는 경우
            elif failure_list and retry_count == 0:
                print("조회를 재시도하였으나 조회하지 못한 코드가 있습니다.")
                print(failure_list)
            else:
                break

        finish_time = time.time()
        duration = finish_time - start_time
        print(f"크롤링에 소요된 시간: {duration}")

        # 결과물을 DataFrame에 입력
        for _ in result_list:
            temp_df = pd.DataFrame(_, index=[_["code"]])
            result_df = pd.concat([result_df, temp_df])

        return result_df.sort_index()

    def naver_movie_basic_info(self, func_args):
        """네이버 영화의 기본 정보를 가져옵니다."""
        # 전달 받은 매개변수를 변수에 대입
        headers = func_args[0]
        code = func_args[1]
        base_url = "https://movie.naver.com/movie/bi/mi/detail.nhn?code="

        # 크롤링한 내용을 저장할 변수 선언
        ko_title = ""
        i18n_title = ""
        release_year = ""
        status = ""

        # 크롤링할 페이지 주소 조합
        target_url = base_url + str(code)

        # Requests 모듈로 페이지 조회
        try:
            req_result = requests.get(target_url, headers=headers)
        # 연결 오류가 발생한 경우
        except ConnectionError:
            # 조회 실패를 출력하고 저장
            print(f"{code}번의 조회를 실패하였습니다.")
            movie_dict = {
                "code": code,
                "ko_title": None,
                "i18n_title": None,
                "release_year": None,
                "status": "Fail",
            }

            # 다음 조회 전까지 4초 미만의 무작위 대기 시간 부여
            # 소수점 이하 시간까지 부여하여 봇 탐지 우회 시도
            time.sleep(random.random() + random.randint(0, 3))

            return movie_dict

        # 조회한 결과를 BeautifulSoup 객체로 변환
        bs_result = BeautifulSoup(req_result.text, "lxml")
        try:
            title_temp = bs_result.find_all("h3", class_="h_movie")

            # 없는 코드를 조회할 경우 이 부분에서 IndexError 발생
            ko_title_string = title_temp[0].a.string
            i18n_title_temp = title_temp[0].strong["title"].replace("\t", "")
            i18n_title_string = i18n_title_temp[:-6]
            release_year_string = i18n_title_temp[-4:]
        # IndexError 처리
        except IndexError:
            ko_title = None
            i18n_title = None
            release_year = None
            status = "OK"
        else:
            ko_title = ko_title_string
            i18n_title = i18n_title_string
            release_year = release_year_string
            status = "OK"
        finally:
            movie_dict = {
                "code": code,
                "ko_title": ko_title,
                "i18n_title": i18n_title,
                "release_year": release_year,
                "status": status,
            }

            # 다음 조회 전까지 4초 미만의 무작위 대기 시간 부여
            # 소수점 이하 시간까지 부여하여 봇 탐지 우회 시도
            time.sleep(random.random() + random.randint(0, 3))

            return movie_dict

    def naver_movie_genre(self):
        """네이버 영화의 장르명과 장르 코드를 가져옵니다."""
        target_url = "https://movie.naver.com/movie/sdb/browsing/bmovie_genre.nhn"
        req_result = requests.get(target_url, headers=self.headers)
        bs_result = BeautifulSoup(req_result.text, "lxml")
        search_result = bs_result.find_all("a", href=re.compile("bmovie.nhn\?genre=\d"))
        genre_text_list = []
        genre_code_list = []

        for _ in search_result:
            # 장르명을 추출하여 리스트에 저장
            genre_text = _.string.rstrip()
            genre_text_list.append(genre_text)
            # 장르별 페이지 주소에서 장르 코드 추출
            href_text_temp = _["href"]
            href_text = re.findall("\d+", href_text_temp)[0]
            genre_code_list.append(href_text)

        # 추출한 장르명과 장르 코드로 DataFrame 생성
        genre_info = {"code": genre_code_list, "genre": genre_text_list}
        genre_df = pd.DataFrame(
            genre_info, index=genre_info["code"], columns=list(genre_info.keys())
        )

        return genre_df


if __name__ == "__main__":
    print("이 파일을 직접 실행할 수 없습니다.")
    print("크롤러를 실행하려면 main.py를 실행하세요.")
    raise SystemExit
