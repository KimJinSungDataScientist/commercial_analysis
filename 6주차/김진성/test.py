import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import folium

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
    # 군집화 5부터 시작해서 약국 위도가 군집안에 없을때까지 무한 반복

    count = 5
    perpect = True
    chk_kmeans = df1['lat'].unique()

    while (perpect):
        count += 1
        # if (count > 100):
        #     count = 5
        print(count)
        kmeans = KMeans(n_clusters=count, random_state=777).fit(loc_df)
        loc_df['label'] = kmeans.labels_

        for i in range(count):
            chk = 0
            for j in loc_df[loc_df['label'] == i]['latitude']:
                if str(j) in chk_kmeans:
                    break
                else:
                    chk += 1
                if chk == len(loc_df[loc_df['label'] == i]):
                    # if chk < 10:  # 10개보다 작은 경우 외곽 지역에서 작은 군집이 추출되는거라
                    #     break
                    perpect = False
                    print("solution label : ", i)
                    solution_label = i
                    break
            if perpect == False:
                break

    temp_long = loc_df[loc_df['label'] == solution_label]['longitude'].mean()
    temp_lati = loc_df[loc_df['label'] == solution_label]['latitude'].mean()

    map = folium.Map(location=[temp_lati, temp_long], zoom_start=16)
    for i in loc_df[loc_df['label'] == solution_label].index:
        folium.CircleMarker(location=[loc_df[loc_df['label'] == solution_label].loc[i, 'latitude'],
                                      loc_df[loc_df['label'] == solution_label].loc[i, 'longitude']],
                            color='#00ff99',
                            fill_color='#00ff99',
                            tooltip=(loc_df[loc_df['label'] == solution_label].loc[i, 'latitude'],
                                     loc_df[loc_df['label'] == solution_label].loc[i, 'longitude']),
                            radius=40
                            ).add_to(map)

    for i in df1.index:
        folium.CircleMarker(location=[df1.loc[i, 'lat'], df1.loc[i, 'long']],
                            color='#808080',
                            fill_color='#808080',
                            tooltip=(df1.loc[i, 'lat'], df1.loc[i, 'long']),
                            radius=40
                            ).add_to(map)

    map.save('solution.html')

kmeans(df)