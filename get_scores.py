import pdb, traceback, sys
import time
import operator
import numpy
from simrank_fns import *
import os
import pickle

def main():
  start_time = time.time()
  cwd = os.getcwd()
  limit = 2000 #limit on number of nodes in graph (both tweets and hashtags)

  #get graph adj list, adj matrix, and the dicts that pair tweets w/ id and hashtags w/ id
  data_file = cwd + '\\data_7_gen_2_plain.txt'
  graph_dict, adj_matrix, tweet_ids, hashtag_ids, index_id = create_graph(data_file, limit) 

  fn_1 = cwd + '\\data_7_gen_2_bigraph.txt'
  sorted_graph = sorted(graph_dict.items())
  make_list_tuples(fn_1,sorted_graph)
  
  fn_2 = cwd + '\\data_7_gen_2_tweets.txt'
  make_list(fn_2,tweet_ids)

  fn_3 = cwd + '\\data_7_gen_2_hashtags.txt'
  sorted_hashtag_ids = collections.OrderedDict(sorted(hashtag_ids.items()))
  make_list(fn_3, sorted_hashtag_ids)

  #store dict option so it can be loaded into hashtag_search.py later
  pickle.dump(graph_dict, open(cwd + '\\data_7_gen_2_bigraph.p', "wb" ))
  pickle.dump(tweet_ids, open(cwd + '\\data_7_gen_2_tweets.p', "wb" ))
  pickle.dump(hashtag_ids, open(cwd + '\\data_7_gen_2_hashtags.p', "wb" ))

  #calculate summed even powers of adj matrix to find which node pairs are within path of len K away
  test = adj_matrix
  for i in range(2): 
    test = numpy.dot(test,test) #range(k) means up to G^(2^(i+1))
    if i != 0:
      sums = sums + test
    else:
      sums = test
  time_pt_1 = time.time() - start_time
  print("Sum even powers of adj matrix: %s seconds" % (time_pt_1))
  for i in range(len(sums)):
    if numpy.count_nonzero(sums[i]) > 0:  #if there exists nonzeros in node
      sums[i,i] += 1 #make the diagonal entry of sums be nonzero so that it is included in id_nonzeros
  
  #get nonzeros of summed even powers of adj matrix to find node pairs which have decently big simrank scores. saves memory.
  #first convert each node into an index #. then convert back. may req 2 hashtables
  nonzeros = numpy.transpose(numpy.nonzero(sums))
  id_nonzeros = index_to_id(nonzeros, index_id)
  time_pt_2 = time.time() - start_time
  print("Calculate Simrank: %s seconds" % (time_pt_2 - time_pt_1))
  
  scores, sorted_scores = simrank(graph_dict, id_nonzeros) #run simrank to get node pair scores
  fn_4 = cwd + '\\data_7_gen_2_scores.txt'
  make_list_tuples(fn_4, sorted_scores)
  pickle.dump(scores, open(cwd + '\\data_7_gen_2_scores.p', "wb" ))


if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
