import pdb, traceback, sys
import time
import operator
import numpy
from simrank_fns import *

def main():
  start_time = time.time()
  #get node_scores, G^2, and the dicts that pair tweets w/ id and hashtags w/ id
  data_file = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 5/data_7_gen_2_plain.txt'
  #graph, tweet_ids, hashtag_ids, graph_dict = create_graph(data_file) #trial 4
  graph_dict, adj_matrix, tweet_ids, hashtag_ids, index_id = create_graph(data_file) 

  filename = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_bigraph_2.txt'
  sorted_graph = sorted(graph_dict.items())
  make_list_tuples(filename,sorted_graph)
  
  filename_2 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_tweets_2.txt'
  make_list(filename_2,tweet_ids)

  filename_3 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_hashtags_2.txt'
  sorted_hashtag_ids = collections.OrderedDict(sorted(hashtag_ids.items()))
  make_list(filename_3, sorted_hashtag_ids)

  test = adj_matrix
  sums = test
  for i in range(2): 
    test = numpy.dot(test,test) #range(k) means up to G^(2^(i+1))
    if i != 0:
      sums = sums + test
    else:
      sums = test

  #first convert each node into an index #. then convert back. may req 2 hashtables
  nonzeros = numpy.transpose(numpy.nonzero(sums))
  id_nonzeros = index_to_id(nonzeros, index_id)
  print("--- %s seconds ---" % (time.time() - start_time))
  
  graph_sq = create_G_sq(graph_dict, id_nonzeros, tweet_ids)  #create G^2 from bipartite graph
  #fn_4 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 6/data_7_gen_2_G_sq.txt'
  #make_list(fn_4, graph_sq)
  print("--- %s seconds ---" % (time.time() - start_time))

  scores, sorted_scores = simrank(graph_dict, graph_sq) #run simrank
  fn_5 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 7/data_7_gen_2_scores_2.txt'
  make_list_tuples(fn_5, sorted_scores)

  print("--- %s seconds ---" % (time.time() - start_time))
  

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
