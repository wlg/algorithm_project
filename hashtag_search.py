import pdb, traceback, sys
import time
import operator
import numpy
from simrank_fns import *

def load_graph(filename):
  graph = {}
  file = open(filename,'r')
  for line in file: 
    splitted = line.split()
    tails = []
    for tail in splitted[2:-1]:
      tails.append(int(tail.replace('[','').replace(']','').replace(',','')))
    graph[int(splitted[0])] = tails
  file.close()
  return graph

def load_ids(filename):
  ids = {}
  file = open(filename,'r')
  for line in file: 
    splitted = line.split()
    if splitted != []:
      ids[int(splitted[0])] = splitted[-1]
  file.close()
  return ids

def load_scores(filename):
  scores = {}
  file = open(filename,'r')
  for line in file: 
    splitted = line.split()
    key = (int(splitted[0][1:-1]), int(splitted[1][:-1])) #remove paren and convert to integer tuple
    scores[key] = float(splitted[-1])
  file.close()
  return scores

def main():
  #load G, scores and id labels
  graph_dict = load_graph('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_bigraph_2.txt')
  tweet_ids = load_ids('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_tweets_2.txt')
  hashtag_ids = load_ids('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_hashtags_2.txt')
  scores = load_scores('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_scores_2.txt')
  
  #from user input, get input_tweet (during create_graph, you assigned an id to input_tweet, so use that)
  #as you're running make_g_sq, find related tweets to speed things up
  #extract hashtags from input tweet

  #rev_tweet_ids = ... #reverse tweet_ids
  #input_tweet = rev_tweet_ids[user_input]
  input_tweet = 7
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
    return 'No results found'

  sorted_rel_scores = sorted(related_tweets.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()
  similar_tweets = sorted_rel_scores[0:100] #get the 100 most similar tweets

  similar_hashtags = []
  for (tweet, score) in similar_tweets:
    hashtags = graph_dict[tweet] #for hashtags of that tweet
    for h in hashtags:
      if h not in input_tweet_hashtags and h not in similar_hashtags: #find relative complement and prevent duplicates
        similar_hashtags.append(h)
  similar_hashtags = list(set(similar_hashtags))
  fn_2 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_tweet_7_simhash_top100_2.txt'
  output = open(fn_2,'w') 
  for h in similar_hashtags:
    output.write(str(hashtag_ids[h]) + '\n')
  output.close()

  #sort hashtags into categories of scores
  #get histogram of scores. take the bottom 25%, middle, and top 25% into 3 separate categories (high, mid, low similarity)
  
if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
