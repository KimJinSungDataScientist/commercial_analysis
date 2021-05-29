import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
from fiona.crs import from_string
import warnings
from collections import defaultdict
warnings.filterwarnings(action='ignore')


# %%
# 위도 =111.195km , 경도 88.8km , 2km 박스일 때 반경  1.414
def dis_to_lat(km):
    return km / 111.195


def dis_to_lon(km):
    return km / 88.8


def lat_to_dis(lat):
    return lat * 111.195


def lon_to_dis(lon):
    return lon * 88.8


def get_xy(data, lon, lat, km):
    lat_size = dis_to_lat(km)
    lon_size = dis_to_lon(km)
    return data[(data['위도'] <= lat + lat_size / 2) & (data['위도'] >= lat - lat_size / 2) &
                (data['경도'] <= lon + lon_size / 2) & (data['경도'] >= lon - lon_size / 2)]


# %%
def get_traffic_light(lon, lat, km):
    global df, df2
    df = pd.read_csv("/Users/chanju/github/smussp/6주차/이찬주/서울시 신호등 관련 정보.csv", encoding='CP949')
    df['X좌표'] = df['X좌표'].astype(float)
    df['Y좌표'] = df['Y좌표'].astype(float)
    df['geometry'] = df.apply(lambda row: Point([row['X좌표'], row['Y좌표']]), axis=1)
    df = gpd.GeoDataFrame(df, geometry='geometry')
    df.crs = from_string("+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=600000 +ellps=GRS80 +units=m +no_defs")
    wgs84 = from_string("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    df = df.to_crs(wgs84)
    df['lon'] = df['geometry'].map(lambda t: t.x)
    df['lat'] = df['geometry'].map(lambda t: t.y)
    df = df.rename({'lat': '위도', 'lon': '경도'}, axis='columns')
    df = df[['신호등수량', '위도', '경도']]
    return get_xy(df, lon, lat, km)


# %%
def get_crosswalk(lon, lat, km):
    global df3
    df3 = pd.read_csv("/Users/chanju/github/smussp/6주차/이찬주/서울시 횡단보도 위치정보 (좌표계_ WGS1984).csv", encoding='CP949')
    df3 = df3.drop(['순번', '상태', '횡단보도종류코드', '가로길이', '세로길이', '화살표시수량', '화살표시길이',
                    '고가', '구경찰서코드', '구코드', '동코드', '지번', '신경찰서코드', '작업구분', '표출구분', '도로구분',
                    '관할사업소', '신규정규화ID', '설치일', '교체일', '이력ID', '공사관리번호', '횡단보도관리번호.1',
                    '공사형태'], axis='columns')
    return get_xy(df3, lon, lat, km)


# %%
def get_bus_stop(lon, lat, km):
    global df4
    df4 = pd.read_csv("/Users/chanju/github/smussp/6주차/이찬주/서울특별시 버스정류소 위치정보.csv", encoding='CP949')
    df4 = df4.drop(['정류소번호'], axis=1)
    df4 = df4.rename({'X좌표': '경도', 'Y좌표': '위도'}, axis=1)
    df4 = df4[['정류소명', '위도', '경도']]

    return get_xy(df4, lon, lat, km)


# %%
def get_subway(lon, lat, km):
    global df5
    df5 = pd.read_csv("/Users/chanju/github/smussp/6주차/이찬주/station_coordinate.csv")
    df5 = df5.drop(['line', 'code'], axis=1)
    df5 = df5.rename({'lat': '위도', 'lng': '경도'}, axis=1)
    return get_xy(df5, lon, lat, km)


# %%
def mean_top10(environment):
    eev_sum = 0
    for i in range(0, 9):
        eev = environment[i]
        eev_sum += len(environment[i])

    mean_ev = eev_sum / 10
    return mean_ev


# %%
def score_ev(mean_tl, mean_cw, mean_bs, mean_sb, target_tl, target_cw, target_bs, target_sb):
    if (mean_tl != 0):
        score_tl = (len(target_tl) / mean_tl)
        if (score_tl > 1):
            score_tl = 1
    else:
        score_tl = 0

    if (mean_cw != 0):
        score_cw = (len(target_cw) / mean_cw)
        if (score_cw > 1):
            score_cw = 1
    else:
        score_cw = 0

    if (mean_bs != 0):
        score_bs = (len(target_bs) / mean_bs)
        if (score_bs > 1):
            score_bs = 1
    else:
        score_bs = 0

    if (mean_sb != 0):
        score_sb = (len(target_sb) / mean_sb)
        if (score_sb > 1):
            score_sb = 1
    else:
        score_sb = 0

    traffic_score = score_tl + score_cw + score_bs + score_sb

    traffic_score = traffic_score * 25

    return traffic_score


# %%
def get_score(test_df, target_lon, target_lat, km):
    tl = []
    cw = []
    bs = []
    sb = []

    for tup in zip(list(test_df['경도']), list(test_df['위도'])):
        tl.append(get_traffic_light(tup[0], tup[1], 1))
        cw.append(get_crosswalk(tup[0], tup[1], 1))
        bs.append(get_bus_stop(tup[0], tup[1], 1))
        sb.append(get_subway(tup[0], tup[1], 1))

    mean_tl = mean_top10(tl)
    mean_cw = mean_top10(cw)
    mean_bs = mean_top10(bs)
    mean_sb = mean_top10(sb)

    target_tl = get_traffic_light(target_lon, target_lat, km)
    target_cw = get_crosswalk(target_lon, target_lat, km)
    target_bs = get_bus_stop(target_lon, target_lat, km)
    target_sb = get_subway(target_lon, target_lat, km)

    traffic_score = score_ev(mean_tl, mean_cw, mean_bs, mean_sb, target_tl, target_cw, target_bs, target_sb)

    return traffic_score