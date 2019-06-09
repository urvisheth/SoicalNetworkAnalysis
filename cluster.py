"""
Cluster data.
"""
import json
from collections import Counter, defaultdict, deque
import copy
from itertools import combinations
import math
import networkx as nx
import urllib.request
import matplotlib.pyplot as plt
import community
import sys
import glob
import os
import time
import community
from sklearn.cluster import spectral_clustering
import scipy

CLASSIFY_FILE_NAME= "classify_friend.json"

def read_file(filename):
    """
    Reading data from file
    """
    array = []
    with open(filename) as f:
        for line in f:
            array.append(json.loads(line))
    return array
    pass
        
def build_graph(users):
    G = nx.Graph()
    for u in users:
        G.add_edges_from([str(u['user_id']), str(fid)] for fid in u['friends'])
    return G

def draw_network(graph, users, filename):
    graph_labels=dict()
    for u in users:
        graph_labels[str(u['user_id'])]=u['user_name']
    fig = plt.figure()
    plt.axis('off')
    nx.draw_networkx(graph,pos=nx.spring_layout(graph),with_labels = True, labels=graph_labels, node_size = 70, width = 0.2)
    fig.savefig(filename, format='png')
    plt.draw() 
    pass

def bfs(graph, root):
    node2distances = defaultdict(int)
    node2num_paths = defaultdict(int)
    node2parents = defaultdict(list)

    nodequeue = deque([root])
    visited = set()
    visited.add(root)

    node2distances[root] = 0
    node2num_paths[root] = 1
    depth = 0
    parent = root
    while (len(nodequeue) > 0):
        node = "".join(nodequeue.popleft())
        depth = node2distances[node] + 1
        for n in graph.neighbors(node):
            if (n not in visited):
                nodequeue.append ([n])
                node2distances[n] = depth
                node2parents[n].append(node)
                node2num_paths[n] = 1
                visited.add(n)
            elif (node2distances[n] == depth):
                node2num_paths[n] += 1
                node2parents[n].append(node)
              
    return dict(sorted(node2distances.items())), dict(sorted(node2num_paths.items())), dict(sorted((_node, sorted(_parents)) for _node, _parents in node2parents.items()))
    pass

def bottom_up(root, node2distances, node2num_paths, node2parents):
    result = dict()
    cnt = Counter()
    for n in sorted(node2distances, key=node2distances.get, reverse=True):
        if n != root:
            if node2num_paths[n] > 1:
                for a in node2parents[n]:
                    finalTuple = tuple(sorted([n, a]))
                    result[finalTuple]=(float)((cnt[n]+1)/len(node2parents[n]))
                    cnt[a]=(float)(cnt[a]+result[finalTuple])
            else:
                l = tuple(sorted([n,node2parents[n][0]]))
                result[l] = float(cnt[n] + 1) 
                cnt[node2parents[n][0]] = (float)(cnt[node2parents[n][0]]+result[l])
    
    return result
    pass

def approximate_betweenness(graph):
    betweenness = dict()
    for n in graph.nodes():
        node2distances, node2num_paths, node2parents = bfs(graph, n)
        botup = bottom_up(n, node2distances, node2num_paths, node2parents)
        for b in botup:
            if b in betweenness:
                betweenness[b] = betweenness[b] + botup[b]
            else:
                betweenness[b] = botup[b]
    for a,b in betweenness.items():
        betweenness[a]=b/2

    return betweenness
    pass

def partition_girvan_newman(graph):
    index=0
    gcopy=graph.copy()
    apxbtw = approximate_betweenness(gcopy)    
    result=sorted(apxbtw.items(),key=lambda x: (-x[1], x[0]))
    compnent =[c for c in nx.connected_component_subgraphs(gcopy)]
    while (True):
        gcopy.remove_edge(*(result[index][0]))
        compnent = [c for c in nx.connected_component_subgraphs(gcopy)]
        if len(compnent) > 1:
            break
        elif len(compnent) == 1:
            index += 1
    return compnent
    pass



def main():
    users = read_file(CLASSIFY_FILE_NAME)
    print("File has been read!")
    graph = build_graph(users)
    print("Graph in progress..... This might take a while...")
    draw_network(graph,users,"cluster_img.png")
    print("Graph Stored in cluster_img.png")
    clusters = partition_girvan_newman(graph)
    print('%d clusters' % len(clusters))
    print('first partition:');
    for i in range(0,len(clusters)):
        print("cluster ",i," has  ",clusters[i].order(),"  nodes")      
    file = open("cluster_data.txt","w")  
    file.write(str(clusters))
    file.close()
    pass

if __name__ == "__main__":
    main()