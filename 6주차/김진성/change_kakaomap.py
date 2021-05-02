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
from folium.plugins import MarkerCluster

def address_to_latitude(address):
    global lat
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
    result = requests.get(urlparse(url).geturl(),
                      headers = {'Authorization': 'KakaoAK {}'.format('c49d80867cade015337852235f9762c7')})
    json_obj = result.json()
    for document in json_obj['documents']:
        lat = document['y']
    return lat

def address_to_longtitude(address):
    global long
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
    result = requests.get(urlparse(url).geturl(),
                      headers = {'Authorization': 'KakaoAK {}'.format('c49d80867cade015337852235f9762c7')})
    json_obj = result.json()
    for document in json_obj['documents']:
         long = document['x']
    return long
hope_upjong = '약국'
local_name = '서울시 성산동'
top10_place = [hope_upjong,'축구장','택배','미용실','고등학교','만화방','낚시','편의점','돈까스','보건소','문방구']
# top10_place = ['미용실']
top10_color = ['red','red','blue','green','purple','orange','beige','pink','gray','cadetblue','darkpurple']
# find =  input('검색할 정보를 입력하세요 : ')


time.sleep(1)

driver = webdriver.Chrome(
    executable_path= '/Users/kimjinsung/Desktop/winwin_plus 2021-1/6주차/김진성/chromedriver'
)


# 핀 꼽기
map = folium.Map(location = [37.541,126.986], zoom_start =8)
# marker_cluster = MarkerCluster().add_to(map) # 이쁘게 군집화해줌


for i in top10_place:
    cnt=0
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
                if(count==5):
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
    data_frame = pd.DataFrame(results, columns=['name', 'address',"lat","long"])
    print(data_frame)



    for a in data_frame.index:
        if top10_place.index(i) == 0: # 창업 희망업종인데 이미 창업되어있는 동일 업종의 위치 원으로 표시
            folium.CircleMarker(location=[data_frame.loc[a, "lat"], data_frame.loc[a, "long"]],
                                radius=100,
                                popup=data_frame.loc[a, "name"],
                                color='#ffffgg',
                                fill_color='#fffggg'
                                ).add_to(map)
        else:
            folium.Marker(location = [data_frame.loc[a,"lat"],data_frame.loc[a,"long"]],
                          popup = data_frame.loc[a,"name"],
                          icon=folium.Icon(color=top10_color[top10_place.index(i)], icon='info-sign')
                          ).add_to(map)

# print(map)

from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>


<div id='maplegend' class='maplegend'
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>

<div class='legend-title'>창업 희망 업종 : 약국 and (연관성 상위 10개 업종)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>축구장</li>
    <li><span style='background:blue;opacity:0.7;'></span>택배</li>
    <li><span style='background:green;opacity:0.7;'></span>미용실</li>
    <li><span style='background:purple;opacity:0.7;'></span>고등학교</li>
    <li><span style='background:orange;opacity:0.7;'></span>만화방</li>
    <li><span style='background:beige;opacity:0.7;'></span>낚시</li>
    <li><span style='background:pink;opacity:0.7;'></span>편의점</li>
    <li><span style='background:gray;opacity:0.7;'></span>돈까스</li>
    <li><span style='background:cadetblue;opacity:0.7;'></span>보건소</li>
    <li><span style='background:darkpurple;opacity:0.7;'></span>문방구</li>
  </ul>
</div>
</div>

</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

map.get_root().add_child(macro)






map.save('solution.html')