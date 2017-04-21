import pdb, traceback, sys
import operator
import numpy
from simrank_fns import *
import os
import pickle

#given an input tweet, find similar hashtags

def get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, similar_tweets, cat):
  similar_hashtags = []
  for (tweet, score) in similar_tweets:
    hashtags = graph_dict[tweet] #for hashtags of that tweet
    for h in hashtags:
      if h not in input_tweet_hashtags and h not in similar_hashtags: #find relative complement and prevent duplicates
        similar_hashtags.append(h)
  similar_hashtags = list(set(similar_hashtags))

  cwd = os.getcwd()
  fn = cwd + '\\data_7_gen_2_tweet_'+str(input_tweet)+'_'+cat+'.txt'
  output = open(fn,'w') 
  if similar_hashtags == []:
    output.write('No new hashtags found')
  else:
    for h in similar_hashtags:
      output.write(str(hashtag_ids[h]) + '\n')
  output.close()

def main():
  #load G, scores and id labels
  cwd = os.getcwd()
  graph_dict = pickle.load( open(cwd + '\\data_7_gen_2_bigraph.p', "rb" ) )
  tweet_ids = pickle.load( open(cwd + '\\data_7_gen_2_tweets.p', "rb" ) ) 
  hashtag_ids = pickle.load( open(cwd + '\\data_7_gen_2_hashtags.p', "rb" ) ) 
  scores = pickle.load( open(cwd + '\\data_7_gen_2_scores.p', "rb" ) ) 

  #from user input, get input_tweet (during create_graph, you assigned an id to input_tweet, so use that)
  #as you're running make_g_sq, find related tweets to speed things up
  #extract hashtags from input tweet

  #rev_tweet_ids = ... #reverse tweet_ids
  #input_tweet = rev_tweet_ids[user_input]
  if sys.argv[1].isdigit() == False:
    return 'Enter a positive integer for system argument'
  input_tweet = int(sys.argv[1])
  #input_tweet_hashtags = ['#hits', '#musique' '#pop', '#np']
  input_tweet_hashtags =  graph_dict[input_tweet] #get hashtag neighbors of input tweet
  
  related_tweets = {}
  stop_signal = 'on'
  for (x,y) in scores: 
    if x != y:
      if x == input_tweet:  #only eval x b/c pairs are symmetrical
        stop_signal = 'off'
        related_tweets[y] = scores[(x,y)] #get all tweets w/ a score > 0 relative to input_tweet

  if stop_signal == 'on':
    return 'No similar tweets found'

  sorted_rel_scores = sorted(related_tweets.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()
  #similar_tweets = sorted_rel_scores[0:100] #get the 100 most similar tweets

  #sort hashtags into categories of scores. The % are arbitrary, for now.
  #get histogram of scores. High: top 10%. Mid: 10-20%. Low: 20-30%
  high = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .1)]
  mid = sorted_rel_scores[int(len(sorted_rel_scores) * .1) : int(len(sorted_rel_scores) * .2)]
  low = sorted_rel_scores[int(len(sorted_rel_scores) * .2) : int(len(sorted_rel_scores) * .3)]
  
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, high, 'high')
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, mid, 'mid')
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, low, 'low')

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
