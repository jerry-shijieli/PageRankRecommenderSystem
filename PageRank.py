#!/usr/bin/env python

# Given a graph (expressed using networkx package), apply PageRank algorithm to it and compute the importance of
# its nodes according to their linkages. For the details of PageRank algorithm, please check the corresponding
# webpage on Wikipedia.

import sys
import operator



def main():
    if len(sys.argv)==1:
        print("Usage: python PageRank.py <data_filename> <directed OR undirected>")
        sys.exit(1)

    data_filename = sys.argv[1]
    isDirected = True if sys.argv[2]=="directed" else False
    graph = read_network_data(data_filename, isDirected)
    pagerank = PageRank(graph, isDirected)
    pagerank.rank()
    ranks_of_page = pagerank.getRanks()
    sorted_ranks = sorted(ranks_of_page.iteritems(), key=operator.itemgetter(1), reverse=True)
    save_filename = data_filename.split('/')[-1].split('.')[0] + ".csv"
    saveResults(sorted_ranks, save_filename)


if __name__ == "__main__":
    main()