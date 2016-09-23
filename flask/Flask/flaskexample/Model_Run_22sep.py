import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sklearn import linear_model, metrics
from sklearn.linear_model import LinearRegression, LogisticRegression
import pickle

plt.close('all')
def rank_by_increase(f):
    dPR=datetime.strptime('2018-05-01', '%Y-%m-%d')
    monthmin=29
    dEN=dPR-relativedelta(months=monthmin)
    dST=dPR-relativedelta(months=monthmin+12)

    pred=np.empty((1,1))
    cur=np.empty((1,1))
    for id_, line in enumerate(f):
        #establish TS
#         print id_
#         continue
        nowJSON=json.loads(line)
        medTS=np.array(nowJSON['medTS'])
        avgTS=np.array(nowJSON['avgTS'])
        dates=[datetime.strptime(item, '%Y-%m-%d') for item in nowJSON['time']]
        TS=avgTS
        try:
                #find id of values
            idEN=next(id_ for id_, obj in enumerate(dates) if obj>dEN)
            idST=next(id_ for id_, obj in enumerate(dates) if obj>dST)
            datesec=np.array([(item-datetime(1970,1,1)).total_seconds() for item in dates])


            predDS=(dPR-datetime(1970,1,1)).total_seconds()
            #create regression
            regr = linear_model.LogisticRegression()
            x_train=np.array(datesec[idST:idEN]).reshape(-1,1)
            y_train=np.array(TS[idST:idEN])

            #calculate
            regr.fit(x_train, y_train)
            cur=np.append(cur, np.nanmean(TS[range(idEN-26,idEN)]))
            pred=np.append(pred, regr.predict(predDS))

        except:
            pred=np.append(pred, np.NAN)
            cur=np.append(cur, np.NAN)

    return pred, cur

def plot_my_buys(f,buys):
    print buys
    fig, ax = plt.subplots(figsize=(9, 4))
    for id_, line in enumerate(f):
        if id_ not in buys:
            continue
#         print id_
        nowJSON=json.loads(line)
        medTS=np.array(nowJSON['medTS'])
        avgTS=np.array(nowJSON['avgTS'])
        dates=[datetime.strptime(item, '%Y-%m-%d') for item in nowJSON['time']]
        TS=avgTS
        ax.plot(dates,avgTS/1000,linestyle='None',marker='.')
    ax.grid()

def main(city):
    filenames=filenames=os.listdir('/Users/samjwil/Projects/Real_Estate/Data/Trulia/json_old')
    del filenames[0]

    for id_, filename in enumerate(filenames):
        if city not in filename:
            continue
    #     if id_<5:
    #         continue
        with open('/Users/samjwil/Projects/Real_Estate/Data/Trulia/jsonfiles_wgeo/' + filename, 'r') as f:
            #rank by percent increase
            pred, cur=rank_by_increase(f)
        pc=np.column_stack((pred, cur))
        # print pc
        percGrowth=np.delete(np.divide(pc[:,0],pc[:,1]),0)
        index=np.argsort(percGrowth)[::-1]
        thresholds=np.array([2e5, 5e5, 1e6])
        buys2=np.empty((1,1))

        try:
            #loop through thresholds, looking for good buys near those values
            for id_, value in enumerate(thresholds):
                print value
                buy=index[np.absolute(cur[index]-value)/value < .2]#20%
                #if exists
                if buy.any():
                    #buys2 append
                    buys2=np.append(buys2,buy[np.where(~np.isnan(percGrowth[buy]))[0][0]])
            buys2=np.delete(buys2,0)

            with open('/Users/samjwil/Projects/Real_Estate/Data/Trulia/jsonfiles_wgeo/' + filename, 'r') as f:
                plot_my_buys(f,buys2.astype(int))
        except:
            continue
#     print stop

main('Portland')
plt.show()
