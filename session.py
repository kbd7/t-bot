# parser.py
import requests
from bs4 import BeautifulSoup
import os

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGIN_URL = 'https://kbdlab.co.kr/index.php?mid=board_fleamarket&act=dispMemberLoginForm'
HOME_URL = 'https://kbdlab.co.kr/index.php?mid=home'
MARKET_URL = 'https://kbdlab.co.kr/index.php?mid=board_fleamarket'
# 로그인할 유저정보를 넣어주자 (모두 문자열)
LOGIN_INFO = {
    'user_id': '',
    'password': ''
}

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:

    # HTTP POST request: 로그인을 위해 POST url와 함께 전송될 data를 넣어주자.
    login_req = s.post(LOGIN_URL, data=LOGIN_INFO)
    # 어떤 결과가 나올까요?
    print(login_req.status_code)
    if login_req.status_code != 200:
        raise Exception('로그인이 되지 않았어요!-아이디와 비밀번호를 다시 한번 확인해 주세요. ')
    
    
# -- 여기서부터는 로그인이 된 세션이 유지됩니다 

    req = requests.get(MARKET_URL)
    req.encoding = 'utf-8' # Clien에서 encoding 정보를 보내주지 않아 encoding옵션을 추가해줘야합니다.

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)

    posts = soup.select('td.title')
    latest = posts[4].text # 0번은 회원중고장터 규칙입니다.

with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f:
        f.write(latest)


# -- 여기서부터는 로그인이 된 세션이 유지됩니다 

