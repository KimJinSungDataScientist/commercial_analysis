import requests
import json
from urllib.parse import urlparse


def getLatLng(key_word):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' + key_word+'&radius=20000&page='

    rest_api_key = 'c49d80867cade015337852235f9762c7'
    header = {'Authorization': 'KakaoAK ' + rest_api_key}

    for i in range(1,4):
        r = requests.get(url+str(i), headers=header)
        result_address = json.loads(r.text)

        for document in result_address['documents']:
            result = document['place_name'], document['category_name'],document["y"], document["x"]
            print(result)

        meta = result_address['meta']
        if (meta['is_end']==True):
            break

    return result_address




print(getLatLng('서울시 치킨집'))

