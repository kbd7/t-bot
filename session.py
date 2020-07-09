# session.py
import requests
from bs4 import BeautifulSoup
import os

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# URL & INFO
LOGIN_URL = 'https://kbdlab.co.kr/index.php?act=procMemberLogin'
MARKET_URL = 'https://kbdlab.co.kr/index.php?mid=board_fleamarket'

LOGIN_INFO = {
    'user_id': '',
    'password': '',
}

header = {
    'Referer' : 'https://kbdlab.co.kr/index.php?mid=board_fleamarket&act=dispMemberLoginForm',
}

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:

    # HTTP POST request: 로그인을 위해 POST url와 함께 전송될 data를 넣어주자.
    res = s.post(LOGIN_URL, data=LOGIN_INFO, headers=header)
    res.raise_for_status()
    
    if res.status_code != 200:
        raise Exception('로그인이 되지 않았어요!-아이디와 비밀번호를 다시 한번 확인해 주세요. ')
    
# -- 여기서부터는 로그인이 된 세션이 유지됩니다 

    req = s.get(MARKET_URL)

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    posts = soup.select('td.title')
    latest = posts[3].text
    print(latest)

with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f:
        f.write(latest)

