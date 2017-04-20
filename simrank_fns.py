import pdb, traceback, sys
import csv
import operator
import collections
import networkx as nx
from networkx.algorithms import bipartite
import numpy

#compute distance between two graphs. If > 5, do not calculate a pair for them
#Create a bipartite graph of tweets and hashtags. Map each tweet to a pos int ID and each hashtag to a neg int ID
def create_graph(data_file):
  lim = 10000
  graph_dict = {}
  adj_matrix = []
  index_id = {} #id : adj matrix row index (later flip them)
  tweet_labels = {}
  hashtag_labels = {}
  i=1 #tweet id
  j = -1 #hashtag id
  n = -1 #start at -1 b/c +1 when new node. index id
  k=1
  f = open(data_file, 'r')
  hashtags = []
  hashtag_labels = {} #id : hashtag
  hashtag_labels_flip = {} #hashtag : id
  for tweet in f:
    if k > lim: #b/c MemoryError
      break
    else:
      if '#' in tweet: #for now, only consider tweets with hashtags in them. 
        tweet_labels[i] = tweet #assign id i as tweet
        adj_matrix.append([0]*lim) #new entry in adj matrix. DON'T DELETE IT EVEN IF EMPTY. keeps track of nodes
        n += 1
        index_id[i] = n #this row in adj matrix is tweet
        graph_dict[i] = [] 
        splitted_tweet = tweet.split()
        for word in splitted_tweet:
          if '#' in word and len(word) > 1: #if hashtag that's not just '#'
            if word not in hashtag_labels_flip:  #if it's a new hashtag
              hashtag_labels[j] = word #assign id j as hashtag
              hashtag_labels_flip[word] = j #assign hashtag as id j
              graph_dict[j] = [i] #new hashtag
              n += 1 #tweets and hashtags are mixed in index ids
              adj_matrix.append([0]*lim) 
              adj_matrix[index_id[i]][n] = 1 #symmetric so only keep track of one side. upper triangular adj matrix
              adj_matrix[n][index_id[i]] = 1
              index_id[j] = n  #this row in adj matrix is tweet
              j -= 1
            #the neighbors of hashtag j (even tho directed graph, this is for algos to know hashtag's neighbors)
            else: #it's an old hashtag
              graph_dict[hashtag_labels_flip[word]].append(i)
              adj_matrix[index_id[i]][index_id[hashtag_labels_flip[word]]] = 1 #[tweet][hashtag]
              adj_matrix[index_id[hashtag_labels_flip[word]]][index_id[i]] = 1
            if word not in graph_dict[i]: #avoid duplicate hashtags. Put this after labeling hashtags to id's
              graph_dict[i].append(hashtag_labels_flip[word]) #add hashtag to neighbors of tweet i
        if graph_dict[i] == []: #just in case tweet only contains words '#' of len 1
          del graph_dict[i]
        else:
          i += 1
    k += 1
  adj_matrix = numpy.delete(adj_matrix, numpy.s_[(n+1)::],1) #delete unused columns
  adj_matrix = numpy.matrix(adj_matrix)
  return graph_dict, adj_matrix, tweet_labels, hashtag_labels, index_id

def index_to_id(nonzeros, index_id):
  index_id = {v: k for k, v in index_id.iteritems()} #index_id : id
  id_nonzeros = {} #faster to check if exists in hash table than in array
  for entry in nonzeros:
    new_entry = (index_id[entry[0]],index_id[entry[1]])
    id_nonzeros[new_entry] = 0
  return id_nonzeros

#Create G^2
def create_G_sq(G, id_nonzeros, tweet_labels):
  G_sq = {}
  for tw_1 in tweet_labels:
    for tw_2 in tweet_labels:
      if (tw_1,tw_2) not in G_sq or (tw_2,tw_1) not in G_sq:
        if (tw_1,tw_2) in id_nonzeros or (tw_2,tw_1) in id_nonzeros: #symmetric
          neighbors = {} #reset neighbors for each new tweet pair
          G_sq[(tw_1,tw_2)] = [] #tweet nodes
          for ht_1 in G[tw_1]:    #add in hashtag pair nodes
            for ht_2 in G[tw_2]:
              if (ht_1,ht_2) not in neighbors or (ht_2,ht_1) not in neighbors:
                neighbors[(ht_1,ht_2)] = []
                G_sq[(tw_1,tw_2)].append((ht_1,ht_2))
              if (ht_1,ht_2) not in G_sq or (ht_2,ht_1) not in G_sq:   #hashtag nodes. if already in graph
                G_sq[(ht_1,ht_2)] = [(tw_1,tw_2)]
              else:
                G_sq[(ht_1,ht_2)].append((tw_1,tw_2))
  return G_sq     

#run SimRank on G^2 to calculate similarity scores
def simrank(G, G_sq):
  C=0.8 #decay factor
  node_scores={}
  for node in G_sq:
    x = node[0]
    y = node[1]
    if x == y:
      node_scores[(x,y)] = 1
    else:
      node_scores[(x,y)] = 0

  for k in range(5): #5 iterations
    for node in G_sq:
      x = node[0] #don't call it a and b b/c messes it up in pdb?
      y = node[1]
      if x != y:
        sim_sum = 0
        for neighbor1 in G[x]:
          for neighbor2 in G[y]:
            if (neighbor1,neighbor2) in node_scores:
              sim_sum += node_scores[(neighbor1,neighbor2)] 
        new_sim = (C/(len(G[x]) * len(G[y]))) * sim_sum
        node_scores[(x,y)] = new_sim

  node_scores = { k:v for k, v in node_scores.items() if v < 1 } #sort by item, so can't use orderedDict
  sorted_scores = sorted(node_scores.items(), key=operator.itemgetter(1))
  sorted_scores.reverse()
  return node_scores, sorted_scores

#take in dictionary and return key : value list
def make_list(filename,input_dict):
  output = open(filename,'w')
  for head in input_dict: 
    row = str(head) + ' : ' + str(input_dict[head])
    output.write(row + '\n')
  output.close()

#take in list of tuples and return key : value list
def make_list_tuples(filename, pair_list):
  output = open(filename,'w')
  for pair in pair_list: 
    row = str(pair[0]) + ' : ' + str(pair[1])
    output.write(row + '\n')
  output.close()

def make_graph_csv(filename, graph_dict,hashtag_labels):
  csv = open(filename,"w")
  for v in graph_dict: 
      row=str(v)
      edges = graph_dict[v]
      for t in edges:
          row += ';' + str(t)
      csv.write(row + '\n')
  #for v in hashtag_labels.values():
    #csv.write(str(v) + '\n')
  csv.close()

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


