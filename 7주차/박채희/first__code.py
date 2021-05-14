import sys
from first import Ui_MainWindow
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
from urllib.parse import urlparse


class find_top10(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.search_button.clicked.connect(self.search_buttonFunc)
        self.show()

    def search_buttonFunc(self):
        text=self.search_input.toPlainText()
        print(text)
        def address_to_latitude(address):
            global lat
            url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
            result = requests.get(urlparse(url).geturl(),
                                  headers={
                                      'Authorization': 'KakaoAK {}'.format('012f3277daabe10113b230330bd12a77')})
            json_obj = result.json()
            for document in json_obj['documents']:
                lat = document['y']
            return lat

        def address_to_longtitude(address):
            global long
            url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
            result = requests.get(urlparse(url).geturl(),
                                  headers={
                                      'Authorization': 'KakaoAK {}'.format('012f3277daabe10113b230330bd12a77')})
            json_obj = result.json()
            for document in json_obj['documents']:
                long = document['x']
            return long


        search_key = text
        options = webdriver.ChromeOptions()  # 크롬 브라우저 옵션
        options.add_argument('headless')  # 브라우저 안 띄우기
        options.add_argument('lang=ko_KR')  # KR 언어

        ######## 바꿔줘야할부분
        driver = webdriver.Chrome('C:/Users/chaeh/chromedriver')

        driver.get('https://map.kakao.com/')
        driver.find_element_by_xpath('/html/body/div[10]/div/div/div/strong').click()
        search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
        search_area.send_keys(search_key)  # 검색어 입력
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="info.search.place.sort"]/li[2]/a').click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find_all('a', class_='link_name')
        li1 = []
        for i in range(10):
            li1.append(title[i]['title'])
        print(li1)

        cat = soup.find_all(class_='subcategory clickable')
        li2 = []
        pattern = '<[^>]*>'
        for i in range(10):
            tp = str(cat[i])
            tp = re.sub(pattern=pattern, repl='', string=tp)
            li2.append(tp)
        print(li2)

        addr = soup.find_all('div', class_='addr')
        li3 = []
        for i in range(10):
            tp = str(addr[i])
            tp = re.sub(pattern=pattern, repl='', string=tp)
            tp = re.search('\n(.*)\n', tp).group(1)
            li3.append(tp)
        print(li3)
        # driver.quit() # driver 종료, 브라우저 닫기

        li4 = []
        li5 = []
        for i in range(10):
            li4.append(address_to_latitude(li3[i]))
            li5.append(address_to_longtitude(li3[i]))

        list = []
        for i in range(10):
            li = []
            li.append(li1[i])
            li.append(li2[i])
            li.append(li3[i])
            li.append(li4[i])
            li.append(li5[i])
            list.append(li)
        df = pd.DataFrame(list, columns=['name', 'type', 'addr', 'lat', 'lng'])
        print(df)


app = QApplication([])
sn = find_top10()
QApplication.processEvents()
sys.exit(app.exec_())