"""
Quick look at Zip code

"""
import ijson

filename='/Users/samjwil/Projects/Real_Estate/Data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
with open(filename) as df:
    parser=ijson.parse(df)
    for prefix in parser:
        print prefix
