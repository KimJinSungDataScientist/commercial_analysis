from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from urllib.parse import urlparse
import pandas as pd
import folium
from Hyun import main_func
from folium.plugins import MarkerCluster

key_commer = 'bG%2BZ%2BmDdiTVy%2Faq2OLF%2FKCockUZQnuHoXbUTjrFJYWbe5ZtQ7qRAJgXoFYaG7YY7N7%2BLkPJhevA1Wy1wdeH%2FIw%3D%3D'

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
hope_upjong = '치킨'
local_name = '서울시 성산동 '
lists = main_func(key_commer,37.577472  ,126.967881)
top10_place = [hope_upjong] +lists
top10_color = ['red','red','blue','green','purple','orange','beige','pink','gray','cadetblue','darkpurple']


time.sleep(10)

driver = webdriver.Chrome(
    executable_path= '/Users/kimjinsung/Desktop/winwin_plus 2021-1/6주차/김진성/chromedriver'
)


# 핀 꼽기
map = folium.Map(location = [37.541,126.986], zoom_start =8)
# marker_cluster = MarkerCluster().add_to(map) # 이쁘게 군집화해줌


for i in top10_place:

    find = local_name + i

    url = "https://m.map.naver.com/"
    driver.get(url)
    action = ActionChains(driver)

    time.sleep(4)
    driver.find_element_by_class_name('Nbox_input_text').click()

    driver.find_element_by_class_name('Nbox_input_text._search_input').send_keys(find)
    driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[2]/button[2]').click()

    time.sleep(4)
    replys =driver.find_elements_by_xpath('//*[@id="ct"]/div[2]/ul/li')
    # print(len(replys)) 찾은 점포 개수

    results = []
    for index, reply in enumerate(replys):
            name = reply.find_element_by_css_selector('div.item_tit').text
            address =reply.find_element_by_css_selector('div.wrap_item').text.split('\n')[1]
            latitude = address_to_latitude(address)
            longtitude = address_to_longtitude(address)
            results.append((name, address, latitude, longtitude))


    data_frame = pd.DataFrame(results, columns=['name', 'address',"lat","long"])
    # print(data_frame)



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

<div class='legend-title'>Legend (연관성 상위 10개 업종)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>축구장</li>
    <li><span style='background:blue;opacity:0.7;'></span>택배</li>
    <li><span style='background:green;opacity:0.7;'></span>미용실</li>
    <li><span style='background:purple;opacity:0.7;'></span>고등학교</li>
    <li><span style='background:orange;opacity:0.7;'></span>만화방</li>
    <li><span style='background:beige;opacity:0.7;'></span>낚시</li>
    <li><span style='background:pink;opacity:0.7;'></span>편의점</li>
    <li><span style='background:gray;opacity:0.7;'></span>카페</li>
    <li><span style='background:cadetblue;opacity:0.7;'></span>한식집</li>
    <li><span style='background:darkpurple;opacity:0.7;'></span>병원</li>

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