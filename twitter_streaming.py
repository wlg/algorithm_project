#Listener code: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import operator
from itertools import islice
import pdb

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'S8XtmVeNeYp0F5s3Ba8294rOD'
consumer_secret = '7qbCN3piFWNMixcKCNgf8jNpv1TR71zWyahm5xq7CGE2o4LI0p'
access_token = '848576341700206592-THBDf8XxuL84ok0bwH7YKovFBFKezTS'
access_token_secret = 'qebXmt5NFERtGEnulgxD7MxIf7HvrXO3Tja2V8l1uVvNE'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

#use hashtags from the last iteration to search for related hashtags in the Listener
def get_hashtags():
  X=7 #dataset ID
  Y=2 #iteration step
  hashtag_freqs = {}
  f = open('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_'+str(X)+'_gen_'+str(Y)+'_plain.txt', 'r')
  for tweet in f:
    if '#' in tweet:  #only consider tweets with hashtags
      splitted_tweet = tweet.split()
      for word in splitted_tweet:
        if word[0] == '#':
          if word in hashtag_freqs:
            hashtag_freqs[word] += 1  #track frequency to take only the top 10 most popular hashtags
          else:
            hashtag_freqs[word] = 1

  hashtag_freqs.pop('#', None)  #remove '#'
  sorted_freqs = sorted(hashtag_freqs.items(), key=operator.itemgetter(1))  #sort 
  sorted_freqs.reverse()
  hashtags = []
  for (k,v) in sorted_freqs:
    hashtags.append(k)
  most_pop = sorted_freqs[0:int(round(len(sorted_freqs)/4))]
  #most_pop_ret = hashtags[0:int(round(len(hashtags)/4))]

  prev_hashtags = []
  if Y > 0: #check if file exists
    with open('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_'+str(X)+'_curr_hashtag_gen_'+str(Y)+'.txt', 'r') as f:
      #prev_hashtags = list(islice(f, Y*10)) #The +'\n' is built in from reading the file
      end = Y*10  #the number of lines to check in the file. The number of hashtags in prev gen Y is Y*10
      j=0
      for line in f:
        if j < end:
          prev_hashtags.append(line.replace('\n',''))
        else:
          break
        j += 1

  new_top_10 = [] #take the top 10 most popular hashtags in this iteration step
  i=0
  while len(new_top_10) < 11:
    if hashtags[i] not in prev_hashtags:  #only add in new hashtags 
      new_top_10.append(hashtags[i])
    i += 1

  most_pop_ret = prev_hashtags + new_top_10 #old hashtags plus top 10 new hashtags
  f2 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_'+str(X)+'_curr_hashtag_gen_'+str(Y+1)+'.txt'
  with open(f2,'w') as f2:
    for hashtag in most_pop_ret:
      f2.write(str(hashtag) + '\n') #store as first line for use in gen Y+2. 

  #store freqs for new hashtags
  filename = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_'+str(X)+'_hashtag_gen_'+str(Y+1)+'.txt'
  with open(filename,'w') as f:
    f.write('number of hashtags: ' + str(len(hashtags)) + '\n')
    #f.write(str(most_pop[399:410])+'\n')
    for hashtag in most_pop:
      f.write(str(hashtag[0]) + ' : ' + str(hashtag[1]) + '\n')
  
  return most_pop_ret

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    keywords = get_hashtags()
    #This line filter Twitter Streams to capture data by the keywords
    #stream.filter(track=['drake','nickiminaj'])
    stream.filter(track=keywords)