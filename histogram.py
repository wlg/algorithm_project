import pdb
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

X=7
Y=1
scores = []
f = open('C:/Users/Michael/Documents/_rsch/classes sp17/algo/project code/trial 7/data_'+str(X)+'_gen_'+str(Y+1)+'_scores_2.txt', 'r')
for line in f:
	splitted = line.split()
	if float(splitted[-1]) > 0.05: #float may cause float(0) to be slightly > 0
		scores.append(float(splitted[-1]))

plt.hist(scores)
plt.show()