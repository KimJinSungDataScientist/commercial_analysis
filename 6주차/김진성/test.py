from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from urllib.parse import urlparse
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# def address_to_latitude(address):
#     global lat
#     url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
#     result = requests.get(urlparse(url).geturl(),
#                       headers = {'Authorization': 'KakaoAK {}'.format('c49d80867cade015337852235f9762c7')})
#     json_obj = result.json()
#     for document in json_obj['documents']:
#         lat = document['y']
#     return lat
#
# def address_to_longtitude(address):
#     global long
#     url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
#     result = requests.get(urlparse(url).geturl(),
#                       headers = {'Authorization': 'KakaoAK {}'.format('c49d80867cade015337852235f9762c7')})
#     json_obj = result.json()
#     for document in json_obj['documents']:
#          long = document['x']
#     return long
hope_upjong = '치킨'
local_name = '서울시 성산동'
top10_place = ['미용실']
top10_color = ['red','red','blue','green','purple','orange','beige','pink','gray','cadetblue','darkpurple']
# find =  input('검색할 정보를 입력하세요 : ')


# time.sleep(10)

driver = webdriver.Chrome(
    executable_path= '/Users/kimjinsung/Desktop/winwin_plus 2021-1/6주차/김진성/chromedriver'
)


# 핀 꼽기
map = folium.Map(location = [37.541,126.986], zoom_start =8)
# marker_cluster = MarkerCluster().add_to(map) # 이쁘게 군집화해줌


from bs4 import BeautifulSoup
cnt=0
chk=1
for i in range(1):
    # find = local_name + i
    find = '서울시 성산동치킨'
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
        print(upjong_lists_name[upjong_lists_addr.index(addr)].attrs['title'])
        print(str(addr.contents[1].contents[0]))
    search_area.clear()

    while(True):
        try:
            if cnt==0:
                driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
                time.sleep(1)
                cnt+=1
            else:
                chk+=5
                driver.find_element_by_xpath('// *[ @ id = "info.search.page.next"]').send_keys(Keys.ENTER)
                time.sleep(1)
                if(driver.find_element_by_xpath('//*[@id="info.search.page.no1"]').text != str(chk)): # 서울 성산동 미용실 이 경우 딱 5개에서 끝나서 끝 인식이 안됨; 이 경우 처리 코드
                    break


            # 2~ 5페이지 읽기
            for i in range(2, 6):
                # 페이지 넘기기
                xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
                driver.find_element_by_xpath(xPath).send_keys(Keys.ENTER)
                time.sleep(1)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                upjong_lists_name = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name')
                place_lists = soup.select('.placelist > .PlaceItem > .info_item > .addr')
                place_lists = soup.select('.Info > .body > .keywordSearch > .pageWrap > .next')

                for addr in place_lists:
                     print(upjong_lists_name[place_lists.index(addr)].attrs['title'])
                     print(str(addr.contents[1].contents[0]))

        except ElementNotInteractableException:
            print('not found')
            break

        finally:
            search_area.clear()