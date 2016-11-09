#!/usr/bin/env python

# Given a graph (expressed using networkx package), apply PageRank algorithm to it and compute the importance of
# its nodes according to their linkages. For the details of PageRank algorithm, please check the corresponding
# webpage on Wikipedia.

import os
import sys
import csv
import operator
import numpy as np
from dataloader import read_network_data, read_demo_data

class PageRank:
    def __init__(self, graph, directed):
        self.graph = graph
        self.V = len(self.graph.nodes()) # number of nodes
        self.E = len(self.graph.edges()) # number of edges
        self.directed = directed
        self.ranks = dict() # page ranks

    def compute_ranks(self, damp=0.85, max_iter=100, tol=1e-6):
        # initialize rankings
        for node, node_attr in self.graph.nodes(data=True):
            if self.directed:
                self.ranks[node] = 1/float(self.V)
            else:
                self.ranks[node] = node_attr.get("rank")
        # update pagerank values over iterations
        count_iter = 0
        error = np.inf
        prev_rank = dict(self.ranks)
        while (count_iter<max_iter and error>tol):
            error = 0.0
            count_iter += 1
            for node in self.graph.nodes():
                rank_sum = 0
                if self.directed:
                    for edge in self.graph.in_edges(node):
                        nd_src = edge[0]
                        out_degree = self.graph.out_degree(nd_src)
                        if out_degree > 0:
                            rank_sum += self.ranks[nd_src] / float(out_degree)
                else:
                    for nd_src in self.graph.neighbors(node):
                        out_degree = self.graph.degree(nd_src)
                        if out_degree > 0:
                            rank_sum += self.ranks[nd_src] / float(out_degree)
                self.ranks[node] = damp*rank_sum + (1-damp)/float(self.V)
                error += (self.ranks[node] - prev_rank[node])**2
            error = np.sqrt(error / float(self.V))
            prev_rank = dict(self.ranks)

    def get_ranks(self):
        return self.ranks

def save_results(ranks, filename):
    save_path = os.path.join('results', filename)
    with open(save_path, 'wb') as fout:
        cwriter = csv.writer(fout, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for rk in ranks:
            cwriter.writerow([str(rk[0]), str(rk[1])])
    fout.close()

def main():
    if len(sys.argv)==1:
        print("Usage: python PageRank.py <data_filename> <directed OR undirected>")
        sys.exit(1)
    data_filename = sys.argv[1]
    isDirected = True if sys.argv[2]=="directed" else False
    graph = read_network_data(data_filename, isDirected)
    pagerank = PageRank(graph, isDirected)
    pagerank.compute_ranks(0.85)
    ranks_of_page = pagerank.get_ranks()
    sorted_ranks = sorted(ranks_of_page.iteritems(), key=operator.itemgetter(1), reverse=True)
    save_filename = data_filename.split('/')[-1].split('.')[0] + ".csv"
    save_results(sorted_ranks, save_filename)


if __name__ == "__main__":
    main()