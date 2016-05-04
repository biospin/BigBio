
# coding: utf-8

# In[8]:

get_ipython().magic(u'matplotlib inline')
from datetime import datetime
import time
import os
from pprint import pprint
import numpy as np
import gzip, cPickle
import theano
import theano.tensor as T
from theano import function
from glob import glob
import timeit
import sys
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA


# In[3]:

def dir_to_dataset(glob_files):
    for file_count, file_name in enumerate( sorted(glob(glob_files)) ):
        print(file_name)
        pklPartial=gzip.open(file_name)
        pklT= cPickle.load(pklPartial)
        if file_count==0:
            dataSet0=pklT[0]
            dataSet1=pklT[1]
        else:
            dataSet0 = np.concatenate((dataSet0,pklT[0]))
            dataSet1 = np.append(dataSet1,pklT[1])
        pklPartial.close()
        print len(dataSet0), len(dataSet1) 

    dataSet1=dataSet1-1
    #print np.amax(dataSet1)
    dataSet= (dataSet0, dataSet1)
    return dataSet


# In[4]:

dataSets = dir_to_dataset('./*type1*')


# In[5]:

X, Y = dataSets


# In[6]:

pca=PCA(n_components=2)


# In[7]:

pX= pca.fit(X).transform(X)


# In[9]:

number = 34
cmap = plt.get_cmap('gnuplot')
colors = [cmap(i) for i in np.linspace(0, 1, number)]


# In[16]:

plt.figure(figsize=(17,17))
for i, c in enumerate(colors):
    plt.scatter(pX[Y == i, 0], pX[Y == i, 1], c=c, label=i)
plt.title('PCA of dataset')
plt.legend()
plt.show()


# In[ ]:



