#Pandas code: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
import json
import pandas as pd
import pdb
import matplotlib.pyplot as plt
import numpy as np

X = 7 #dataset ID
Y = 1 #iteration step
tweets_data_path = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_'+str(X)+'_gen_'+str(Y+1)+'.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line) #dictionary object
        if u'text' in tweet: #some tweets don't have the key 'text'
            tweets_data.append(tweet)
    except:
        continue

tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data) #create 'text' column in dataframe

import io
f = open('C:/Users/Michael/Documents/_rsch/classes sp17/algo/project code/trial 2/data_'+str(X)+'_gen_'+str(Y+1)+'_plain.txt', 'w')
for line in tweets['text']:
    lamp = line.encode('UTF-8') #convert to unicode
    lamp_2 = lamp.decode('unicode_escape').encode('ascii','ignore')	#get rid of unicode artifacts in hashtags
    f.write(lamp_2.replace('\n',' ') + '\n' + '\n') #'\n' within a tweet may break a single tweet into multiple lines
    #so first remove \n bc we want to keep each tweet on one line
