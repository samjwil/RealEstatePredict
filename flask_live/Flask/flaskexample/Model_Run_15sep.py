"""
To Be run from Flask.
To Predict which Real Estate decisions from 2016 will be the most profitable.
"""


#Imports
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import json
from pyzipcode import ZipCodeDatabase

#My definitions.

def samNormalize(I_array):
    normval=np.nanmean(I_array)
    return np.divide(I_array,normval)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#load feature, outputs dataframe
#features: slope
def main(zips):

    featfile='../../../../Data/Model_Runs/Model_15sept.pkl'
    df=pd.read_pickle(featfile)
    #load model
    regzips=df['zip'].values
    slope=df['slope'].values
    ints=df['intercept'].values

    idzips=[np.where(regzips==z)[0][0] for z in zips if z in regzips]

    clf = joblib.load('../../../../Data/Model_Runs/LinearRegression.pkl')

    #build inputs
    ip1=slope[idzips]
    flag=np.where(np.isnan(ip1))
    ip=ip1[~np.isnan(ip1)]
    ip=np.reshape(ip,[ip.shape[0],1])
    #run model
    op=clf.predict(list(ip))
    op=samNormalize(op)

    #return ZipCodeDatabase
    zipnew=np.asarray(zips)
    zips=regzips[idzips][np.where(op>1.1)]
    zjson=[]

    zcdb=ZipCodeDatabase()
    for zid in zips:
        z=zcdb[zid]
        temp= {'lat': z.latitude, 'lng': z.longitude, 'name':z.city}#'zip':int(z.zip),
        zjson.append(temp)
        # zjson=zjson.append(dict({'zip':z.zip, 'lat': z.latitude, 'lon': z.longitude}))
    # print str(json.dumps(zjson))
    return json.dumps(zjson)



# print main([92037, 92037,92037,92037,94101, 90005, 90006, 90007,94102, 94103, 94104, 94105, 94106, 94107, 94108, 94109, 94110, 94111, 94112, 94114, 94115, 94116, 94117, 94118, 94119, 94120, 94121, 94122, 94123, 94124, 94125, 94126, 94127, 94128, 94129, 94130, 94131, 94132, 94133, 94134, 94135, 94136, 94137, 94138, 94139, 94140, 94141, 94142, 94143, 94144, 94145, 94146, 94147, 94150, 94151, 94152, 94153, 94154, 94155, 94156, 94157, 94159, 94160, 94161, 94162, 94163, 94164, 94165, 94166, 94167, 94168, 94169, 94170, 94171, 94172, 94175, 94177, 94188])
    #apply model to input zip codes



#___init___
