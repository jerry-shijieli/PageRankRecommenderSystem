# Given csv data file of network, build directed/undirected graph with nodes end edges from the data file

import networkx as nx
import re
import csv

def read_network_data(datafilename, isDirected):
    with open(datafilename, 'r') as fin:
        creader = csv.reader(fin, delimiter=',')
        data = [row for row in creader]
    print "Reading data and building graph ... "
    if isDirected:
        return build_directed_graph(data)
    else:
        return build_undirected_graph(data)


def build_directed_graph(data):
    pass


def build_undirected_graph(data):
    pass