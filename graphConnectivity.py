#!/usr/bin/env python
# coding: utf-8

"""
File: project.py
------------------------
One important characteristic of a graph is its connectivity.
The vertex (edge) connectivity of a graph is the minimum number of vertices 
that if removed results in a disconnected graph.
Given a graph G, it is well known that the vertex connectivity is
no larger than the edge connectivity which is no larger than the
minimum of the vertex degrees in the graph.
This project is part of an effort to demonstrate that a graph is 4 vertex connected.
The example graph we use is 4 regular which means each vertex has degree 4.
Since the vertex connectivity <= edge connectivity <= 4, if we can show that
the vertex connectivity is not 1, 2 or 3, then the vertex and edge 
connectivity must both be 4.
The procedure systematically removes all k-subsets of vertices from the graph.
To test whether the resulting subgraph is connected, we find its representation 
as an adjacency matrix and then work with powers of this matrix.
"""
NUM_VERTS=8
#our graphs are assumed to have vertices 0,1,...,NUM_VERTS
ADJ_LIST=[[1,4,6,7],[0,2,3,7],[1,3,4,6],[1,2,4,5],[0,2,3,5],
            [3,4,6,7],[0,2,5,7],[0,1,5,6]]
UP_TO=4 # connectivity will be checked from 1 up to "UP_TO"

import numpy as np
import itertools
import copy

def main():
    for i in range(1,UP_TO+1):
        subsets=findsubsets(range(NUM_VERTS),i)
        out=[]
        for j in range(len(subsets)):
            adj_list=copy.deepcopy(ADJ_LIST)
            removed=removeVerts(adj_list,subsets[j])
            reindexed=reindex(removed,subsets[j])
            out.append(isConnected(AL2AM(reindexed)))
        print("The graph is",i,"connected:", all(out))

def findsubsets(orig_set, subset_size):#find subsets of subset_size taken from orig_set
    return list(itertools.combinations(orig_set, subset_size))

"""
This procedure removes the vertices in "subset" from a graph and requires 2 steps: 
    1. remove the list of adjacent vertices for each deleted vertex;
    2. remove the deleted vertices from each of the other lists of adjacent vertices.
"""
def removeVerts(adjList,subset): 
    for i in range(len(subset)):#1st removes the adjacency list corresponding to each of the removed vertices 
        del adjList[subset[-i-1]] #we access the subset backwards
    for lis in adjList:#for the remaining lists, deletes any appearance of a removed vertices
        for j in subset:
            if j in lis:
                lis.remove(j)
    return adjList

"""
To be able to determine connectivity for the graph with vertices
removed, we reindex so that vertices are 0,1,2,..... 
Before doing so, we find the vertex set, the complement of the subset
of vertices removed. Note the use of l_of_l_multi_replace.
"""
def reindex(adjList,subset):
    out=[]
    for ele in range(NUM_VERTS):
        if ele not in subset:
            out.append(ele)
    new_num_verts=NUM_VERTS-len(subset)
    return l_of_l_multi_replace(adjList,out,range(new_num_verts))

"""
To define l_of_l_multi_replace, we nest several functions.
The first function inputs a list, a digit to replace and the replacing digit.
"""

def my_replace(lis,dig1,dig2):#in the list "lis", "dig1" gets replaced with "dig2"
    out=[]
    slis=[]
    for item in lis:
        slis.append(str(item))
    sdig1=str(dig1)
    sdig2=str(dig2)
    for item in slis:
        out.append(int(item.replace(sdig1,sdig2)))
    return out

"""
The next function makes multiple replacements in a single list.
"""
def multi_replace(lis,lis1,lis2):
    for i in range(len(lis1)):
        lis=my_replace(lis,lis1[i],lis2[i])
    return lis
"""
Finally, we apply multiple replacements to a list of lists.
"""

def l_of_l_multi_replace(l_of_l,lis1,lis2):
    out=[]
    for lis in l_of_l:
        out.append(multi_replace(lis,lis1,lis2))
    return out
"""
Before we check to see if a graph is connected, we convert the
form from an adjacency list to an adjacency matrix.
"""
def AL2AM(list):#adjacency list to adjacency matrix converter
    numVerts=len(list)
    A=np.zeros((numVerts,numVerts),dtype=int)
    for i in range(numVerts):
        for j in list[i]:
            A[i,j]=1
    return A

"""
Next step is to create a function to determine whether a graph is connected.
We make use of numpy here by taking the powers of the adjacency matrix.
The fact we are using is that the i,jth entry of a power provides counts 
for walks from  vertex i to vertex j. If there are n vertices,
then if one vertex hasn't been reached by a paths up to length n-1,
then the vertices i and j are not connected.
"""
def isConnected(A):#inputs an adjacency matrix and decides whether graph is connected
    numVerts=len(A)
    out=A#we will be adding the various powers of A to out. At the end, 
    #the entry out_ij will be the number of paths of length up to n-1 that go from vertex i to vertex j
    power=A
    for i in range(1,len(A)):
        power=power.dot(A)
        out=out+power
    out=out.astype('bool') #we replace the counts with the boolean: O goes to False, all nonzero entries go to True
    return all(list(out.flatten()))#this will only output true if the entire matrix is filled with True.
    #Logically "all" corresponds to "and".

if __name__ == '__main__':
    main()
