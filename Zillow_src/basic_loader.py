"""
Try my hand at loading and understanding Zillow Data.


"""
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')
filename='/Users/samjwil/Projects/Real_Estate/Data/Zillow/Zip_MedianListingPricePerSqft_AllHomes.csv'

with open(filename) as f:
    df=pd.read_csv(f, header=0)

# plt.figure()
# plt.plot(df.iloc[:,6:72])

df2=df.iloc[0:100,6:-1]
print df2
df2.transpose().plot()
plt.show()
