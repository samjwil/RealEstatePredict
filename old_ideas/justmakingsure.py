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

for id_, filename in enumerate(filenames):
    print filename
#     continue
#     if 'Portland' not in filename:
#         continue
#     fig, ax=plt.subplots(nrows=1,ncols=1)

    with open('../../Data/Trulia/jsonfiles_wgeo/' + filename, 'r') as f:
        #open a city
        fulldf=pd.DataFrame()
        predactu=np.empty((1,3))
        for kd_, line in enumerate(f):
            nowJSON=json.loads(line)
            medTS=np.array(nowJSON['medTS'])
            avgTS=np.array(nowJSON['avgTS'])
#             date=[datetime.strptime(item, '%Y-%m-%d') for item in nowJSON['time']]
            dates=[str(item) for item in nowJSON['time']]
            TS=cleanTrulia(dates,avgTS)
            TS=returnFullTS(fulldates,dates,TS).reshape([1,-1])

            fulldf=fulldf.append(pd.DataFrame(TS,columns=fulldates))
#             fulldf.concat()
#             print stop
        print stop
#                 date=nowJSON['time']

#                 df=pd.DataFram(avgTS,)


                
