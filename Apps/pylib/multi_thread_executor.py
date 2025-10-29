# multi_thread_executor.py
# 작업을 멀티스레드로 처리할 수 있도록 해주는 모듈

import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
