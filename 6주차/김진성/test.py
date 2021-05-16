import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans\

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
        lati.append((float(i) - 37) * 100)

    long = []
    for i in longitude:
        long.append((float(i) - 126) * 100)

    # plt.figure(figsize=(10, 10))
    # plt.scatter(long, lati)

    loc_df = pd.DataFrame()
    loc_df['longitude'] = long
    loc_df['latitude'] = lati

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
                        # 우선 무지성으로 10개 미만 군집은 제외했음
                        break
                    perpect = True
                    print("solution label : ", i)
                    solution_label = i
            if perpect == True:
                break

    plt.figure(figsize=(15, 15))

    for label in loc_df.label:
        if label == solution_label:
            plt.plot(loc_df.longitude[loc_df.label == label], loc_df.latitude[loc_df.label == label], markersize=20,
                     marker='.')
        else:
            plt.plot(loc_df.longitude[loc_df.label == label], loc_df.latitude[loc_df.label == label], '.')
    plt.show()

kmeans(df)