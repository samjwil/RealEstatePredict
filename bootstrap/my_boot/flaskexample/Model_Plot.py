
import numpy as np
import json
import os
import pandas as pd
from datetime import datetime

def cleanTrulia(dates,TS):
    udates=np.unique(dates)
    newTS=np.empty(udates.shape[0])
    for id_, item in enumerate(udates):
        index=[jd_ for jd_, jtem in enumerate(dates) if jtem==item]
        newTS[id_]=np.nanmean(TS[index])
    return newTS

def returnFullTS(fulldates,dates,TS):
    TS=TS.astype(float)
    for id_, d in enumerate(fulldates):
#         print d
        if d not in dates:
            TS=np.insert(TS,id_,np.NAN)
    return TS

def samSmoothTS(TS,numsmooth):

    new=np.empty(TS.size)

    for id_ in range(new.size-numsmooth):
        print np.nanmean(TS[id_:(id_+numsmooth)])
        index=id_+numsmooth/2
        new[index]=np.nanmean(TS[id_:(id_+numsmooth)])

    return new

def samRemoveNANS(time,TS):
    stack=np.column_stack((time,TS))
    stack=stack[~np.isnan(stack).any(axis=1)]
    return stack[:,0],stack[:,1]

def samLinearFit(time,TS,id_,numback, deg):
    time=time[(id_-numback):id_]
    TS=TS[(id_-numback):id_]
    time,TS = samRemoveNANS(time,TS)
    if not time.any():
        return np.empty(deg)*np.NAN
    p=np.polyfit(time,TS,deg-1)
#     print p
#     plt.plot(time,TS,linestyle='None',marker='.')
#     plt.plot(time,time*p[0]+p[1])
#     plt.show()
    return p

def samTop(val,num):
    num=val[~np.isnan(val)].size*num
    #remove nans from argsort
    i1=np.argsort(val)
    v1=val[i1]
    i2=i1[~np.isnan(v1)]
    id2=i2.size-num

    #return the appropriate values
    if id2<0:
        return i2 #edge case of too large request for non-nans

    return i2[id2:]

def samPolyEval(predtime,p):
    pred=np.zeros(p.shape[0])
    for id_,ptem in enumerate(p.T[::-1,:]):
        new=np.multiply(ptem,np.power(predtime, id_))
        pred-=new
    return pred

def main(city):
    filenames=os.listdir('flaskexample/Data/')

    fulldates=['2009-07-04', '2009-07-11', '2009-07-18', '2009-07-25', '2009-08-01', '2009-08-08', '2009-08-15', '2009-08-22', '2009-08-29', '2009-09-05', '2009-09-12', '2009-09-19', '2009-09-26', '2009-10-03', '2009-10-10', '2009-10-17', '2009-10-24', '2009-10-31', '2009-11-07', '2009-11-14', '2009-11-21', '2009-11-28', '2009-12-05', '2009-12-12', '2009-12-19', '2009-12-26', '2010-01-02', '2010-01-09', '2010-01-16', '2010-01-23', '2010-01-30', '2010-02-06', '2010-02-13', '2010-02-20', '2010-02-27', '2010-03-06', '2010-03-13', '2010-03-20', '2010-03-27', '2010-04-03', '2010-04-10', '2010-04-17', '2010-04-24', '2010-05-01', '2010-05-08', '2010-05-15', '2010-05-22', '2010-05-29', '2010-06-05', '2010-06-12', '2010-06-19', '2010-06-26', '2010-07-03', '2010-07-10', '2010-07-17', '2010-07-24', '2010-07-31', '2010-08-07', '2010-08-14', '2010-08-21', '2010-08-28', '2010-09-04', '2010-09-11', '2010-09-18', '2010-09-25', '2010-10-02', '2010-10-09', '2010-10-16', '2010-10-23', '2010-10-30', '2010-11-06', '2010-11-13', '2010-11-20', '2010-11-27', '2010-12-04', '2010-12-11', '2010-12-18', '2010-12-25', '2011-01-01', '2011-01-08', '2011-01-15', '2011-01-22', '2011-01-29', '2011-02-05', '2011-02-12', '2011-02-19', '2011-02-26', '2011-03-05', '2011-03-12', '2011-03-19', '2011-03-26', '2011-04-02', '2011-04-09', '2011-04-16', '2011-04-23', '2011-04-30', '2011-05-07', '2011-05-14', '2011-05-21', '2011-05-28', '2011-06-04', '2011-06-11', '2011-06-18', '2011-06-25', '2011-07-02', '2011-07-09', '2011-07-16', '2011-07-23', '2011-07-30', '2011-08-06', '2011-08-13', '2011-08-20', '2011-08-27', '2011-09-03', '2011-09-10', '2011-09-17', '2011-09-24', '2011-10-01', '2011-10-08', '2011-10-15', '2011-10-22', '2011-10-29', '2011-11-05', '2011-11-12', '2011-11-19', '2011-11-26', '2011-12-03', '2011-12-10', '2011-12-17', '2011-12-24', '2011-12-31', '2012-01-07', '2012-01-14', '2012-01-21', '2012-01-28', '2012-02-04', '2012-02-11', '2012-02-18', '2012-02-25', '2012-03-03', '2012-03-10', '2012-03-17', '2012-03-24', '2012-03-31', '2012-04-07', '2012-04-14', '2012-04-21', '2012-04-28', '2012-05-05', '2012-05-12', '2012-05-19', '2012-05-26', '2012-06-02', '2012-06-09', '2012-06-16', '2012-06-23', '2012-06-30', '2012-07-07', '2012-07-14', '2012-07-21', '2012-07-28', '2012-08-04', '2012-08-11', '2012-08-18', '2012-08-25', '2012-09-01', '2012-09-08', '2012-09-15', '2012-09-22', '2012-09-29', '2012-10-06', '2012-10-13', '2012-10-20', '2012-10-27', '2012-11-03', '2012-11-10', '2012-11-17', '2012-11-24', '2012-12-01', '2012-12-08', '2012-12-15', '2012-12-22', '2012-12-29', '2013-01-05', '2013-01-12', '2013-01-19', '2013-01-26', '2013-02-02', '2013-02-09', '2013-02-16', '2013-02-23', '2013-03-02', '2013-03-09', '2013-03-16', '2013-03-23', '2013-03-30', '2013-04-06', '2013-04-13', '2013-04-20', '2013-04-27', '2013-05-04', '2013-05-11', '2013-05-18', '2013-05-25', '2013-06-01', '2013-06-08', '2013-06-15', '2013-06-22', '2013-06-29', '2013-07-06', '2013-07-13', '2013-07-20', '2013-07-27', '2013-08-03', '2013-08-10', '2013-08-17', '2013-08-24', '2013-08-31', '2013-09-07', '2013-09-14', '2013-09-21', '2013-09-28', '2013-10-05', '2013-10-12', '2013-10-19', '2013-10-26', '2013-11-02', '2013-11-09', '2013-11-16', '2013-11-23', '2013-11-30', '2013-12-07', '2013-12-14', '2013-12-21', '2013-12-28', '2014-01-04', '2014-01-11', '2014-01-18', '2014-01-25', '2014-02-01', '2014-02-08', '2014-02-15', '2014-02-22', '2014-03-01', '2014-03-08', '2014-03-15', '2014-03-22', '2014-03-29', '2014-04-05', '2014-04-12', '2014-04-19', '2014-04-26', '2014-05-03', '2014-05-10', '2014-05-17', '2014-05-24', '2014-05-31', '2014-06-07', '2014-06-14', '2014-06-21', '2014-06-28', '2014-07-05', '2014-07-12', '2014-07-19', '2014-07-26', '2014-08-02', '2014-08-09', '2014-08-16', '2014-08-23', '2014-08-30', '2014-09-06', '2014-09-13', '2014-09-20', '2014-09-27', '2014-10-04', '2014-10-11', '2014-10-18', '2014-10-25', '2014-11-01', '2014-11-08', '2014-11-15', '2014-11-22', '2014-11-29', '2014-12-06', '2014-12-13', '2014-12-20', '2014-12-27', '2015-01-03', '2015-01-10', '2015-01-17', '2015-01-24', '2015-01-31', '2015-02-07', '2015-02-14', '2015-02-21', '2015-02-28', '2015-03-07', '2015-03-14', '2015-03-21', '2015-03-28', '2015-04-04', '2015-04-11', '2015-04-18', '2015-04-25', '2015-05-02', '2015-05-09', '2015-05-16', '2015-05-23', '2015-05-30', '2015-06-06', '2015-06-13', '2015-06-20', '2015-06-27', '2015-07-04', '2015-07-11', '2015-07-18', '2015-07-25', '2015-08-01', '2015-08-08', '2015-08-15', '2015-08-22', '2015-08-29', '2015-09-05', '2015-09-12', '2015-09-19', '2015-09-26', '2015-10-03', '2015-10-10', '2015-10-17', '2015-10-24', '2015-10-31', '2015-11-07', '2015-11-14', '2015-11-21', '2015-11-28', '2015-12-05', '2015-12-12', '2015-12-19', '2015-12-26', '2016-01-02', '2016-01-09', '2016-01-16', '2016-01-23', '2016-01-30', '2016-02-06', '2016-02-13', '2016-02-20', '2016-02-27', '2016-03-05', '2016-03-12', '2016-03-19', '2016-03-26', '2016-04-02', '2016-04-09', '2016-04-16', '2016-04-23', '2016-04-30', '2016-05-07', '2016-05-14', '2016-05-21', '2016-05-28', '2016-06-04']

    indates=range(len(fulldates))
    dates_plot=[datetime.strptime(item, '%Y-%m-%d') for item in fulldates]

    # num=14
    for id_, filename in enumerate(filenames):
        print (city in filename)
        print filename

        if city not in filename:
            continue
    #     continue
    #     continue
    #     if 'Portland' not in filename:
    #         continue
    #     fig, ax=plt.subplots(nrows=1,ncols=1)

        print filename
        with open('flaskexample/Data/' + filename, 'r') as f:

            print filename
            #open a city
            fulldf=pd.DataFrame()
            fullnp=pd.DataFrame()
            predactu=np.empty((1,3))
            lat=[]
            lng=[]
            names=[]
            ids=[]
            for kd_, line in enumerate(f):
                nowJSON=json.loads(line)
                # print nowJSON
                # print stop
    #             print stop
                medTS=np.array(nowJSON['medTS'])
                avgTS=np.array(nowJSON['avgTS'])
                geo = json.loads(nowJSON['geo'])
                geoname='%s, %s' %(nowJSON['city'], nowJSON['state'])

                lat.append(geo[0]['geometry']['location']['lat'])
                lng.append(geo[0]['geometry']['location']['lng'])
                names.append(nowJSON['name'])
                ids.append(nowJSON['id_'])
                dates=[str(item) for item in nowJSON['time']]

                TS=cleanTrulia(dates,avgTS)
                TS=returnFullTS(fulldates,dates,TS).reshape([1,-1])

                fulldf=fulldf.append(pd.DataFrame(TS,columns=fulldates))


        break





    new=fulldf.interpolate()
    fulldf2=new.T.rolling(window=5,center=False, min_periods=1).mean().T

    numprops=fullnp.mean(axis=0,skipna=True)

    # print stop
    # check percentage change for every neighborhoods
    # I want to iterate through months, and project forward 2 years
    numyears=1

    ignore=(fullnp.mean(axis=1).values<10)
    My=np.empty(len(indates))*np.NAN
    Best=np.empty(len(indates))*np.NAN
    Mean=np.empty(len(indates))*np.NAN
    for id_ in indates:
        if id_<52:
            continue

        if id_==(len(indates)-numyears*52):
            break


        predtime=id_+numyears*52

        deg=2
        pf=np.empty([fulldf.shape[0],deg])*np.NAN
        jd_=-1
        #iterate through rows
        for jd_tr,row in fulldf.iterrows():
            jd_+=1
            if not row.values[~np.isnan(row.values)].any():
                continue
            #apply polyfit
            pf[jd_,:] = samLinearFit(np.asarray(indates), row.values, id_, 26, deg)
        #establish current
        Current=fulldf2.iloc[:,id_].values

        #ignore very small neighborhoods
        pf[ignore,:]=np.NAN
        Current[ignore]=np.NAN

        #make predictions (or realizations)
        Next=fulldf2.iloc[:,predtime].values
        mypred2=samPolyEval(predtime,pf)

        #use my predictions
        percpred=np.divide(mypred2,Current)
        percinc=np.divide(Next,Current)

        #Mine, Best, Mean
        My[id_]=np.nanmean(percinc[samTop(percpred,.1)])
        Best[id_]=np.nanmean(percinc[samTop(percinc,.1)])
        Mean[id_]=np.nanmedian(percinc)


    #####
    #make Prediction
    pf_pred=np.empty([fulldf.shape[0],deg])*np.NAN
    jd_=-1
    for jd_tr,row in fulldf.iterrows():
        jd_+=1
        if not row.values[~np.isnan(row.values)].any():
            continue
        #apply polyfit
        pf_pred[jd_,:] = samLinearFit(np.asarray(indates), row.values, fulldf.shape[1], 26, deg)

    pf[ignore,:]=np.NAN
    Current[ignore]=np.NAN

    mypred2=samPolyEval(predtime,pf)
    percpred=np.divide(mypred2,Current)

    index=samTop(percpred,.2)

    #check thresholds
    thr=[0 ,1e5, 5e5, 1e6, 2e6]
    # bt=np.empty(len(thr))*np.NAN
    btnames=[' ',' ',' ',' ']
    btid=[' ',' ',' ',' ']
    btlat=[]
    btlng=[]
    #red, yellow, green, blue,
    btcols=['ffffff','ffffff','ffffff','ffffff']
    cols=['db1818', 'd0d32e', '0ad618', '4286f4']
    mcol=[]
    for id_,low in enumerate(thr[0:-1]):
        high =thr[1:][id_]
        avail=index[(Current[index]>low) & (Current[index]<high)]
        if not avail.any():
            continue

        bt=int(avail[-1])
        # print bt[id_]
        btnames[id_]= names[int(bt)]
        btid[id_]= str(ids[int(bt)])
        btlat.append(lat[bt])
        btlng.append(lng[bt])
        btcols[id_]=cols[id_]
        mcol.append(cols[id_])


    # plt.close('all')
    x=['"x"'] + np.asarray(fulldates)[~np.isnan(My)].tolist()
    out1=['"My Prediction"'] + My[~np.isnan(My)].astype(str).tolist()
    out2=['"Best Option"'] + Best[~np.isnan(My)].astype(str).tolist()
    out3=['"Market Median"'] + Mean[~np.isnan(My)].astype(str).tolist()
    lat=[str(item) for item in btlat]
    lng=[str(item) for item in btlng]
    mcol=[str(item) for item in mcol]
    x = {'range':["$0 to $100K","$100K to $500K","$500K to $1M","$1M to $2M"], 'name': btnames, 'id_': btid,'cols':btcols}


    output={
        'x': x,
        'out1': out1,
        'out2': out2,
        'out3': out3,
        'lat': lat,
        'lng':lng,
        'result_dict':x,
        'mcol': mcol,
        'geoname':geoname
        }
    return output
    # fig, ax=plt.subplots(ncols=1, nrows=1, )
    # ax.plot(dates_plot,My,linestyle='-',marker='')
    # ax.plot(dates_plot,Best,linestyle='-',marker='')
    # ax.plot(dates_plot,Mean,linestyle='-',marker='')
    # ax.legend(['My Prediction','Best Choices','Market Median'])
    # ax.set_xticklabels(['2011','','2012','','2013','','2014','','2015'])
    # ax.set_title('Two-Year Return on Investment',fontsize=15)
    # ax.set_ylabel('Return on Investment',fontsize=13)

    # plotstr='valid_fig.png'
    # fig.savefig('flaskexample/static/' + plotstr)


    # plt.show()
    # make estimation

    # check how much money is made.

    # find maximum money made
