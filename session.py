# session.py
import requests
from bs4 import BeautifulSoup
import os

import telegram
import time

# 토큰을 지정해서 bot을 선언해줌
my_token = ''

bot = telegram.Bot(token = my_token)
chat_id = bot.getUpdates()[-1].message.chat.id

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# URL & INFO
LOGIN_URL = 'https://kbdlab.co.kr/index.php?act=procMemberLogin'
MARKET_URL = 'https://kbdlab.co.kr/index.php?mid=board_fleamarket'

LOGIN_INFO = {
    'user_id': '',
    'password': ''
}

header = {
    'Referer' : 'https://kbdlab.co.kr/index.php?mid=board_fleamarket&act=dispMemberLoginForm',
}

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:

    # HTTP POST request
    res = s.post(LOGIN_URL, data=LOGIN_INFO, headers=header)
    res.raise_for_status()
    
    if res.status_code != 200:
        raise Exception('로그인이 되지 않았어요!-아이디와 비밀번호를 다시 한번 확인해 주세요. ')
    
# -- 여기서부터는 로그인이 된 세션이 유지됩니다 

while True:
    # HTTP GET request
    req = s.get(MARKET_URL)
    req.encoding = 'utf-8'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    posts = soup.select('td.title')
    latest = posts[3].text
#   print(latest)

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.read()
#      print('before : ' + before)
        if before != latest:
            bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요 ' + latest)
#        else: # just check 
#           bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')
        f_read.close()

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f:
        f.write(latest)

    time.sleep(10) # 초 단위 현재 10초 
