from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from urllib.parse import urlparse
import pandas as pd
import folium
from Hyun import main_func
from sklearn.cluster import KMeans
from folium.plugins import MarkerCluster


def address_to_latitude(address):
    global lat
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    result = requests.get(urlparse(url).geturl(),
                          headers={'Authorization': 'KakaoAK {}'.format('c49d80867cade015337852235f9762c7')})
    json_obj = result.json()
    for document in json_obj['documents']:
        lat = document['y']
    return lat


def address_to_longtitude(address):
    global long
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    result = requests.get(urlparse(url).geturl(),
                          headers={'Authorization': 'KakaoAK {}'.format('c49d80867cade015337852235f9762c7')})
    json_obj = result.json()
    for document in json_obj['documents']:
        long = document['x']
    return long

key_commer = 'bG%2BZ%2BmDdiTVy%2Faq2OLF%2FKCockUZQnuHoXbUTjrFJYWbe5ZtQ7qRAJgXoFYaG7YY7N7%2BLkPJhevA1Wy1wdeH%2FIw%3D%3D'

hope_upjong = '카페'
local_name = '상명대학교 근처 '

top10_place = [hope_upjong,'치킨','피자','샌드위치','이발소']

time.sleep(1)

driver = webdriver.Chrome(
    executable_path='/Users/kimjinsung/Desktop/winwin_plus 2021-1/6주차/김진성/chromedriver'
)

# 핀 꼽기
map = folium.Map(location=[37.541, 126.986], zoom_start=8)
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
    chk2 = True
    while (chk2):
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
                cnt+=1
                if(cnt>8):
                    chk2=False
                    break
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
        folium.CircleMarker(location=[loc_df[loc_df['label'] == solution_label].loc[i,'latitude'],loc_df[loc_df['label'] == solution_label].loc[i,'longitude']],
                            color='#50BCDF',
                            fill_color='#B9EEFF',
                            radius=50,
                            icon=folium.Icon(color='blue', icon='info-sign')
                      ).add_to(map)
    # icon = folium.Icon(color='blue', icon='info-sign')
    from branca.element import Template, MacroElement


    map.save('solution.html')

kmeans(df)