# crawler.py

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import random
import re
import requests
import os
import pandas as pd
import time


class Crawler:
    def __init__(self, settings):
        self.total_workers = os.cpu_count() * 5
        self.executor = ThreadPoolExecutor(max_workers=self.total_workers)
        self.iheaders = settings['iheaders']

    def thread_executor(self, func):
        # 최종 취합 결과물을 저장할 DataFrame 선언
        result_df = pd.DataFrame()
        # 시작 시간 기록
        start_time = time.time()
        # 조회 시작값 입력
        start_point = int(input('시작 번호를 입력하세요: '))
        # 조회 끝값 입력
        end_point = int(input('끝 번호를 입력하세요: '))
        # range 대입
        search_range = range(start_point, end_point + 1)
        print(f'총 {len(search_range)}개를 크롤링합니다.')
        # 멀티쓰레드 처리를 위한 튜플 대입
        func_args = ((self.iheaders, page_code) for page_code in search_range)
        result_list = []
        retry_count = 3

        while True:
            if type(search_range) == int:
                tqdm_total = search_range
            else:
                tqdm_total = len(search_range)
            tqdm_list = list(tqdm(self.executor.map(func, func_args), total=tqdm_total))
            # 조회 실패한 코드 목록 선언
            failure_list = []
            # 실패한 코드를 저장
            for dict_ in tqdm_list:
                if dict_['status'] == 'Fail':
                    failure_list.append(dict_['code'])
                else:
                    result_list.append(dict_)
            if failure_list and retry_count != 0:
                func_args = ((self.iheaders, page_code) for page_code in failure_list)
                search_range = len(failure_list)
                print('실패한 내역이 있어, 재조회를 시도합니다.')
                print(failure_list)
                retry_count -= 1
                continue
            elif failure_list and retry_count == 0:
                print('조회를 재시도하였으나 조회하지 못한 코드가 있습니다.')
                print(failure_list)
            else:
                break

        finish_time = time.time()
        duration = finish_time - start_time
        print(f'크롤링에 소요된 시간: {duration}')

        # 결과물을 DataFrame에 입력
        for _ in result_list:
            temp_df = pd.DataFrame(_, index=[_['code']])
            result_df = pd.concat([result_df, temp_df])

        return result_df.sort_index()

    def naver_movie_basic_info(self, func_args):
        # 전달 받은 매개변수를 변수에 대입
        iheaders = func_args[0]
        code = func_args[1]
        base_url = 'https://movie.naver.com/movie/bi/mi/detail.nhn?code='
        # 크롤링한 내용을 저장할 변수 선언
        ko_title = ''
        i18n_title = ''
        release_year = ''
        status = ''
        # 크롤링할 페이지 주소 조합
        target_url = base_url + str(code)
        # Requests 모듈로 페이지 조회
        try:
            req_result = requests.get(target_url, headers=iheaders)
        # 연결 오류가 발생한 경우
        except ConnectionError:
            print(f'{code}번의 조회를 실패하였습니다.')
            ko_title = None
            i18n_title = None
            release_year = None
            # 조회 실패 상태임을 저장
            status = 'Fail'
            movie_dict = {'code': code, 'ko_title': ko_title,
                          'i18n_title': i18n_title, 'release_year': release_year, 'status': status}
            time.sleep(random.random() + random.randrange(0, 3))
            return movie_dict

        # 조회한 결과를 BeautifulSoup 객체로 변환
        bs_result = BeautifulSoup(req_result.text, 'lxml')
        try:
            title_temp = bs_result.find_all('h3', class_='h_movie')
            # 없는 코드를 조회할 경우 이 부분에서 IndexError 발생
            ko_title_string = title_temp[0].a.string
            i18n_title_temp = title_temp[0].strong['title'].replace('\t', '')
            i18n_title_string = i18n_title_temp[:-6]
            release_year_string = i18n_title_temp[-4:]
        # IndexError 처리
        except IndexError:
            ko_title = None
            i18n_title = None
            release_year = None
            status = 'OK'
        else:
            ko_title = ko_title_string
            i18n_title = i18n_title_string
            release_year = release_year_string
            status = 'OK'
        finally:
            movie_dict = {'code': code, 'ko_title': ko_title,
                          'i18n_title': i18n_title, 'release_year': release_year, 'status': status}
            time.sleep(random.random() + random.randrange(0, 3))
            return movie_dict

    def naver_movie_genre(self):
        target_url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_genre.nhn'
        req_result = requests.get(target_url, headers=self.iheaders)
        bs_result = BeautifulSoup(req_result.text, 'lxml')
        search_result = bs_result.find_all('a', href=re.compile('bmovie.nhn\?genre=\d'))
        genre_text_list = []
        genre_code_list = []
        genre_df = pd.DataFrame()

        for _ in search_result:
            genre_text = _.string.rstrip()
            genre_text_list.append(genre_text)
            pattern = re.compile('\d+')
            href_text_temp = _['href']
            href_text = pattern.findall(href_text_temp)[0]
            genre_code_list.append(href_text)
            genre_info = {'code': genre_code_list, 'genre': genre_text_list}
            genre_df = pd.DataFrame(genre_info, index=genre_info['code'], columns=list(genre_info.keys()))

        return genre_df
