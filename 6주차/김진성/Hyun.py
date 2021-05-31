import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import requests


rest_api_key = 'c09c78655acb25593e9c6f07b0f42f90'
key_commer = 'bG%2BZ%2BmDdiTVy%2Faq2OLF%2FKCockUZQnuHoXbUTjrFJYWbe5ZtQ7qRAJgXoFYaG7YY7N7%2BLkPJhevA1Wy1wdeH%2FIw%3D%3D'
lon =126.955009
lat =37.6027953
km = 2
radius = 707


#위도 =111.195km , 경도 88.8km , 2km 박스일 때 반경  1.414
def dis_to_lat(km):
    return km/111.195
def dis_to_lon(km):
    return km/88.8

def lat_to_dis(lat):
    return lat*111.195
def lon_to_dis(lon):
    return lon*88.8

def get_xy(data,lon, lat,km):
    lat_size = dis_to_lat(km)
    lon_size = dis_to_lon(km)
    return data[(data['위도']<=lat+lat_size/2) & (data['위도']>=lat-lat_size/2) &
                 (data['경도']<=lon+lon_size/2) & (data['경도']>=lon-lon_size/2)]



def get_commer(api_key, cx, cy, km):
    pageNo = 1
    commercial_info = []
    col = ''
    radius = (km/2)*707
    while pageNo<3:
        url = 'http://apis.data.go.kr/B553077/api/open/sdsc/storeListInRadius?radius=%s&cx=%s&cy=%s&serviceKey=%s&pageNo=%s'%(radius, cx, cy, api_key, pageNo)
        response = requests.get(url)
        result = response.text
        soup = BeautifulSoup(result,'lxml')
        col = soup.columns.text.split(',')

        if soup.resultcode.text == '00':
            for item in soup.find_all('item'):
                commercial_info.append(item.text.split('\n')[1:][:-1])
            pageNo += 1
        else:
            break

    if len(commercial_info) > 0:
        commercial_info = pd.DataFrame(commercial_info, columns=col)
    else:
        commercial_info = pd.DataFrame()
    commercial_info = commercial_info.astype({'경도':'float','위도':'float'})
    commercial_info = get_xy(commercial_info, cx, cy, km/2)

    tmp = list(commercial_info['상권업종중분류명'].value_counts().index[:10])
    commercial_info = commercial_info[commercial_info['상권업종중분류명'].isin(tmp)]
    strrr = []
    for i in tmp:
        st =  i.split('/')
        sss = []
        for x in st:
            if len(x)>=2:
                sss.append(x)
        strrr.append(sss[0])
    commercial_info['상권업종중분류명'] =commercial_info['상권업종중분류명'].replace(tmp,strrr)
    commercial_info = commercial_info[['상권업종중분류명','경도','위도']]
    return commercial_info, strrr

# example)
#get_commer(key_commer,lon,lat,2)


# kakao
def search_category(key,category_group_code, x, y, radius=None, rect=None, page=None, size=None, sort=None):
    headers = {"Authorization": "KakaoAK {}".format(key)}
    URL_cat = "https://dapi.kakao.com/v2/local/search/category.json"
    """
    06 카테고리 검색
    """
    params = {'category_group_code': f"{category_group_code}",
              'x': f"{x}",
              'y': f"{y}"}

    if radius != None:
        params['radius'] = f"{radius}"
    if rect != None:
        params['rect'] = f"{rect}"
    if page != None:
        params['page'] = f"{page}"
    if size != None:
        params['size'] = f"{size}"
    if sort != None:
        params['sort'] = f"{sort}"

    res = requests.get(URL_cat, headers=headers, params=params)
    document = json.loads(res.text)
    return document

def get_public(cat,lon,lat):
    radius = 707
    col = ['category_group_name', 'x','y']
    for page in range(1,4):
        if page == 1:
            result = search_category(rest_api_key,cat, lon, lat, radius,page)
            results = pd.DataFrame(result['documents'])[col]
            if result['meta']['is_end'] == True:
                break

        else:
            result = search_category(rest_api_key,cat, lon, lat, radius,page)
            results.append(pd.DataFrame(result['documents'])[col])
            if result['meta']['is_end'] == True:
                break

    results = results.rename(columns = {'x': '경도','y':'위도'})
    results = results.astype({'경도':'float','위도':'float'})
    return results

def main_func(key_commer,lon,lat):
    commer , _= get_commer(key_commer,lon,lat,2)
    commer = commer.append(get_public('SC4',lon, lat))
    commer = commer.append(get_public('BK9',lon, lat))
    commer = commer.append(get_public('CT1',lon, lat))
    commer = commer.append(get_public('PO3',lon, lat))
    commer = commer.append(get_public('AT4',lon, lat))
    commer = commer.append(get_public('HP8',lon, lat))

    strrrr = commer['상권업종중분류명'].value_counts()
    return strrrr[:10]
# example)
# SC4   학교
# BK9   은행
# CT1   문화시설
# PO3   공공기관
# AT4   관광명소
# HP8   병원
# 공원
