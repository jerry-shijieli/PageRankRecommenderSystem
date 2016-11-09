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
    dg = nx.DiGraph() # directed graph
    for entry in data:
        node_dst = entry[0].strip('"')
        val_dst = digits(entry[1])
        node_src = entry[2].strip('"')
        val_src = digits(entry[3])
        edge_weight = val_dst - val_src
        if edge_weight >= 0:
            dg.add_edge(node_src, node_dst, weight=1)
        else:
            dg.add_edge(node_dst, node_src, weight=1)
    return dg


def build_undirected_graph(data):
    udg = nx.Graph()
    nodes = [entry[0] for entry in data]
    edges = [(entry[0], entry[2]) for entry in data]
    rank = 1/float(len(nodes))
    udg.add_nodes_from(nodes, rank=rank)
    udg.add_edges_from(edges, weight=1)
    return udg


def digits(val):
    return int(re.sub("\D", "", val))