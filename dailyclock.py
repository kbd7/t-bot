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

# URL & INFO
MARKET_URL = 'https://dailyclack.com/products/gmk-dracc?_pos=1&_sid=82a43f244&_ss=r'

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:
    while True:
        # HTTP GET request
        req = s.get(MARKET_URL)
        req.encoding = 'utf-8'

        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        posts = soup.select('#AddToCartText-product-template')
        print(posts)
        print(posts[0].text)

        if 'Sold Out' in posts[0].text:
            print('Okay')
            bot.sendMessage(chat_id=chat_id, text='Sold out ' + MARKET_URL)
        else:
            #print('Fail')
            #Just Check
            #bot.sendMessage(chat_id=chat_id, text='수량이 들어왔습니다. ' + MARKET_URL)
        time.sleep(10) # 초 단위 현재 10초 
