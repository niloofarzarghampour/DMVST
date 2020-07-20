#Extract weather data
import pandas as pd
import  numpy  as  np
import codecs

WC = '../wc.vocab'

time_weather = pd.read_csv('../byhour_201601_NY.CSV', encoding='gbk')

#Extract time and weather conditions
col_names = time_weather.columns.tolist()
data_time_wc = time_weather[[col_names[0], col_names[1], col_names[14]]]
data_time_wc = data_time_wc.fillna({col_names[14]: 'Clear'})

data_str = data_time_wc[col_names[0]].tolist()
time_str = data_time_wc[col_names[1]].tolist()
wc_str = data_time_wc[col_names[14]].tolist()

#Time is UTC, New York should subtract 5 hours,
#The UTC time corresponding to one day is a certain time in New York of the previous day, which is regarded as 0 o'clock of this New York day
wc_2018_1 = []
for  i  in  range ( len ( wc_str )):
    tempdata = int(data_str[i].split('/')[0])
    temptime = int(time_str[i].split('Z')[0]) - 5
    if temptime <= 0:
        temptime = 0
    if wc_str[i] == 'Clear':
        tempu  =  1
    elif wc_str[i] == 'Scattered clouds':
        tempu  =  2
    elif wc_str[i] == 'Few clouds':
        tempu  =  3
    elif wc_str[i] == 'Cloudy':
        tempu  =  4
    elif wc_str[i] == 'Overcast':
        tempu  =  5
    elif wc_str[i] == 'Few clouds, mnist':
        tempu  =  6
    elif wc_str[i] == 'fog':
        tempu  =  7
    elif wc_str[i] == 'rain':
        tempu  =  8
    elif wc_str[i] == 'snow':
        tempu  =  9
    elif wc_str[i] == 'Overcast, mist':
        tempu  =  10
    elif wc_str[i] == 'Overcast, rain':
        tempu  =  11
    elif wc_str[i] == 'Overcast, snow':
        tempu  =  12
    wc_2018_1.append([tempdata, temptime, tempwc])

counts_wc = [[[0] * 48] * 266] * 31
counts_wc = np.array(counts_wc)
for  i  in  range ( 31 ):
    for  j  in  range ( 266 ):
        tp = []
        tp = np.array(tp)
        for k in range(4):
            if wc_2018_1[i * 4 + 3 - k][1] == 16:
                start = 48 - (24 - 16) * 2
                end = 47
            elif  wc_2018_1 [ i  *  4  +  3  -  k ] [ 1 ] ==  10 :
                start = 32 - (16 - 10) * 2
                end = 31
            elif  wc_2018_1 [ i  *  4  +  3  -  k ] [ 1 ] ==  4 :
                start = 20 - (10 - 4) * 2
                end = 19
            elif  wc_2018_1 [ i  *  4  +  3  -  k ] [ 1 ] ==  0 :
                start = 8 - (4 - 0) * 2
                end = 7
            temp = [wc_2018_1[i * 4 + 3 - k][2]] * (end - start + 1)
            temp = np.array(temp)
            # if tp[0]==0:
            #     tp=temp
            # else:
            tp = np.hstack((tp, temp))
        counts_wc[30-i][j]=tp

#Save the processed environmental data characteristics to the wc.vocab file
counts_wc_str = []
data = ""
for  i  in  range ( 31 ):
    for  j  in  range ( 266 ):
        for k in range(48):
            if k < 47:
                data = data + str(counts_wc[i][j][k]) + ' '
            else:
                data = data + str(counts_wc[i][j][k])
        counts_wc_str.append(data)
        data = ""

with codecs.open(WC, 'w', 'utf-8') as file_output:
    for data in counts_wc_str:
        file_output.write(data + '\n')