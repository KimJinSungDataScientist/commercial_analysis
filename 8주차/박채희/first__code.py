import sys
from first import Ui_MainWindow
from top10 import Ui_SubWindow
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
import time
from Hyun import main_func
from PyQt5 import uic
from collections import defaultdict
import folium
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from sklearn.cluster import KMeans


key_commer = 'bG%2BZ%2BmDdiTVy%2Faq2OLF%2FKCockUZQnuHoXbUTjrFJYWbe5ZtQ7qRAJgXoFYaG7YY7N7%2BLkPJhevA1Wy1wdeH%2FIw%3D%3D'
'''
class print_top10(QDialog):
    def __init__(self,parent):
        super(print_top10,self).__init__(parent)
        option_ui='C:\\Users\\chaeh\\Untitled Folder\\print_top10.ui'
        uic.loadUi(option_ui,self)
        self.show()
        '''

class print_top10(QMainWindow, Ui_SubWindow):
    def __init__(self, parent=None):
        super(print_top10, self).__init__(parent)
        self.setupUi(self)
        self.label.setText(str(df[['이름','주소']]))
df=[[]]

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
                                      'Authorization': 'KakaoAK {}'.format('c09c78655acb25593e9c6f07b0f42f90')})
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
        driver = webdriver.Chrome('C:/Users/chaeh/chromedriver',options=options)

        driver.get('https://map.kakao.com/')
        driver.find_element_by_xpath('/html/body/div[10]/div/div/div/strong').click()
        search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
        search_area.send_keys(search_key)  # 검색어 입력
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="info.search.place.sort"]/li[2]/a').click()
        time.sleep(1)
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
        global df
        df = pd.DataFrame(list, columns=['이름', '업종종류', '주소', '위도', '경도'])
        df = df.astype({'위도':'float', '경도':'float'})
        print(df)
        driver.quit()
        fdf=df.copy()
        fdf=fdf.drop(['이름','업종종류','주소'],axis=1)
        ls = []

        for x in range(2):
            print(x,'번째')
            ls.append(main_func(key_commer,df['경도'].iloc[x],df['위도'].iloc[x]))
            print(ls[x])
        print(ls)
        dic = defaultdict(int)
        tmp = ls[0]
        print(tmp)
        for x in range(1, len(ls)):
            tmp = tmp.append(ls[x])
        print(tmp)
        val = tmp.values.tolist()
        print(val)
        idx = tmp.index.tolist()
        print(idx)
        for i in range(len(tmp)):
            dic[idx[i]] += val[i]
        print(dic)
        dic = sorted(dic)
        print(dic)
        dic = dic[::-1]
        print(dic)
        dic = dic[:10]
        print(dic)

        hope_upjong = text.split(' ')[2]
        local_name = text.split(' ')[0]+text.split(' ')[1]
        lists = dic
        top10_place = [hope_upjong] + lists

        time.sleep(1)

        driver = webdriver.Chrome(
            executable_path='C:/Users/chaeh/chromedriver'
        )

        # 핀 꼽기
        #map = folium.Map(location=[37.541, 126.986], zoom_start=8)
        # marker_cluster = MarkerCluster().add_to(map) # 이쁘게 군집화해줌

        for i in top10_place:
            cnt = 0
            name = []
            address = []
            find = local_name + i

            url = "https://map.kakao.com/"
            driver.get(url)
            action = ActionChains(driver)

            search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
            search_area.send_keys(find)  # 검색어 입력
            driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
            time.sleep(1)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            upjong_lists_name = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name')
            upjong_lists_addr = soup.select('.placelist > .PlaceItem > .info_item > .addr')
            for addr in upjong_lists_addr:
                name.append(upjong_lists_name[upjong_lists_addr.index(addr)].attrs['title'])
                address.append(str(addr.contents[1].contents[0]))
                # print(upjong_lists_name[upjong_lists_addr.index(addr)].attrs['title'])
                # print(str(addr.contents[1].contents[0]))
            search_area.clear()
            chk = 1
            while (True):
                try:
                    if cnt == 0:
                        driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
                        time.sleep(1)
                        cnt += 1
                    else:
                        chk += 5
                        driver.find_element_by_xpath('// *[ @ id = "info.search.page.next"]').send_keys(Keys.ENTER)
                        time.sleep(1)
                        if (driver.find_element_by_xpath('//*[@id="info.search.page.no1"]').text != str(chk)):
                            # 서울 성산동 미용실 이런 경우 딱 5개에서 끝나서 끝 인식이 안됨, 클릭이 씹혀버림; 이 경우 처리 코드
                            break
                        time.sleep(1)

                    # 2~ 5페이지 읽기
                    for count in range(2, 6):
                        # 페이지 넘기기
                        xPath = '//*[@id="info.search.page.no' + str(count) + '"]'
                        driver.find_element_by_xpath(xPath).send_keys(Keys.ENTER)
                        time.sleep(1)

                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        upjong_lists_name = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name')
                        place_lists = soup.select('.placelist > .PlaceItem > .info_item > .addr')

                        for addr in place_lists:
                            name.append(upjong_lists_name[place_lists.index(addr)].attrs['title'])
                            address.append(str(addr.contents[1].contents[0]))
                            # print(upjong_lists_name[place_lists.index(addr)].attrs['title'])
                            # print(str(addr.contents[1].contents[0]))
                        if (count == 5):
                            driver.find_element_by_xpath('//*[@id="info.search.page.next"]')

                except ElementNotInteractableException:
                    print('not found')
                    break

                finally:
                    search_area.clear()

            results = []
            for count in range(len(name)):
                latitude = address_to_latitude(address[count])
                longtitude = address_to_longtitude(address[count])
                results.append((name[count], address[count], latitude, longtitude))

            # print(results)

            #
            #
            #

            data_frame = pd.DataFrame(results, columns=['name', 'address', "lat", "long"])
            # print(data_frame)
            data_frame.to_csv('DB.csv', mode='a', encoding="utf-8-sig")

        df = pd.read_csv('DB.csv')

        def kmeans(df):
            save_index = df[df['lat'] == 'lat'].index.to_list()
            cnt = 0

            for i in range(len(save_index)):
                globals()['df{}'.format(i + 1)] = df[cnt:save_index[i]].reset_index(drop=True)
                globals()['df{}'.format(i + 1)].drop(columns=df.columns[:-2], inplace=True)
                cnt = save_index[i] + 1
                if i == (len(save_index) - 1):
                    globals()['df{}'.format(i + 2)] = df[cnt:].reset_index(drop=True)
                    globals()['df{}'.format(i + 2)].drop(columns=df.columns[:-2], inplace=True)

            longitude = []
            latitude = []

            for i in range(len(save_index) + 1):
                print(i + 1)
                longitude.append((globals()['df{}'.format(i + 1)].long).to_list())
                latitude.append((globals()['df{}'.format(i + 1)].lat).to_list())

            longitude = sum(longitude, [])
            latitude = sum(latitude, [])

            lati = []
            for i in latitude:
                lati.append(float(i))

            long = []
            for i in longitude:
                long.append(float(i))

            loc_df = pd.DataFrame()
            loc_df['longitude'] = long
            loc_df['latitude'] = lati
            print(loc_df.head())
            # 군집화 5부터 시작해서 약국 위도가 군집안에 없을때까지 무한 반복

            count = 5
            perpect = False

            while (perpect == False):
                count += 1

                kmeans = KMeans(n_clusters=count, random_state=777).fit(loc_df)
                loc_df['label'] = kmeans.labels_

                for i in range(count):
                    chk = 0
                    for j in loc_df[loc_df['label'] == i]['latitude']:
                        if str(j / 100 + 37) in df1['lat'].unique():
                            break
                        else:
                            chk += 1
                        if chk == len(loc_df[loc_df['label'] == i]):
                            if chk < 20:  # 10개보다 작은 경우 외곽 지역에서 작은 군집이 추출되는거라
                                break
                            perpect = True
                            print("solution label : ", i)
                            solution_label = i
                    if perpect == True:
                        break
            print(loc_df[loc_df['label'] == solution_label]['longitude'].mean())
            # for i in range(loc_df[loc_df['label'] == solution_label].shape[0]):
            #     print(loc_df[loc_df['label'] == solution_label]['longitude'].values[i],loc_df[loc_df['label'] == solution_label]['latitude'].values[i])
            temp_long = loc_df[loc_df['label'] == solution_label]['longitude'].mean()
            temp_lati = loc_df[loc_df['label'] == solution_label]['latitude'].mean()

            import folium
            from folium.plugins import MarkerCluster
            map = folium.Map(location=[temp_lati, temp_long], zoom_start=15)
            # center=[90.89695237,56.86138421]
            # folium.Marker(location=center)
            for i in loc_df[loc_df['label'] == solution_label].index:
                # folium.Marker(,icon=folium.Icon(icon='cloud')).add_to(map)
                folium.CircleMarker(location=[loc_df[loc_df['label'] == solution_label].loc[i, 'latitude'],
                                              loc_df[loc_df['label'] == solution_label].loc[i, 'longitude']],
                                    color='#50BCDF',
                                    fill_color='#B9EEFF',
                                    radius=50,
                                    icon=folium.Icon(color='blue', icon='info-sign')
                                    ).add_to(map)
            # icon = folium.Icon(color='blue', icon='info-sign')
            from branca.element import Template, MacroElement

            map.save('solution.html')

        kmeans(df)
        #self.newWindow = print_top10(self)
        #self.newWindow.show()
app = QApplication([])
sn = find_top10()
QApplication.processEvents()
sys.exit(app.exec_())
