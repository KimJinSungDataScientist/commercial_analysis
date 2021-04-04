import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote


xmlUrl = 'http://apis.data.go.kr/B553077/api/open/sdsc/'
My_API_Key = unquote('HkrPPG6in4atPJOdIYi8%2FXi88%2BGIwbJIHxL5RCca%2FL43BHV43cGNDFGIWH7P72zO06mGVxrLfpIQg6cpBH8Iiw%3D%3D')

upjong_operation = pd.read_csv('upjong_api_list.csv')
upjong_operation.drop(columns = 'Unnamed: 3',axis=1,inplace=True)
upjong_operation.columns = ['index','eng','kor']

upjong_operation.set_index('index',drop=True,inplace=True)

print(upjong_operation)

print('\n 원하는 메뉴 index번호 입력 : ')
save_num = ''
# input(save_num)
save_num = '13'


save_num = upjong_operation.iloc[int(save_num)][0]
xmlUrl+=save_num

# 13번 업종별 상가업소 조회 오퍼레이션 명세를 예시로 구성하겠음
# divld : 대분류는 indsLclsCd, 중분류는 indsMclsCd, 소분류는 indsSclsCd를 사용
# key : divld 에 맞춰 넣어줘야하는 업종 코드값
# numOfRows : 페이지당 건수, 최대 1000
# pageNo : 현재 요청 페이지 번호
# type : xml or json


queryParams = '?' + urlencode(    # get 방식으로 쿼리를 분리하기 위해 '?'를 넣은 것이다. 메타코드 아님.
    {
        quote_plus('divId') : 'indsLclsCd',
        quote_plus('key'): 'Q',
        quote_plus('numOfRows'): '10',
        quote_plus('pageNo') : '1',
        # quote_plus('type') : 'xml',
        quote_plus('ServiceKey') : My_API_Key
    }
)
print(xmlUrl + queryParams)

response = requests.get(xmlUrl + queryParams).text.encode('utf-8')
xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
rows = xmlobj.findAll('item')

# print(columns[0].name)
# print(columns[0].text)

rowList = []
nameList = []
columnList = []
rowsLen = len(rows)

for i in range(0, rowsLen):
    columns = rows[i].find_all()

    columnsLen = len(columns)
    for j in range(0, columnsLen):
        if i == 0:
            nameList.append(columns[j].name)

        columnList.append(columns[j].text)
    rowList.append(columnList)
    columnList = []  # 다음 row의 값을 넣기 위해 비워준다. (매우 중요!!)

result = pd.DataFrame(rowList, columns=nameList)
print(result.head())