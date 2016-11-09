# Given csv data file of network, build directed/undirected graph with nodes end edges from the data file

import networkx as nx
import re
import csv

def read_network_data(datafilename, isDirected):
    with open(datafilename, 'r') as fin:
        print "Reading data and building graph ... "
        data = [x.strip().split('\t') for x in fin.readlines()]
        data = data[1:] # remove the header
    fin.close()
    if isDirected:
        dg = nx.DiGraph()
        for entry in data:
            dg.add_edge(entry[0], entry[1])
        return dg
    else:
        udg = nx.Graph()
        for entry in data:
            udg.add_edge(entry[0], entry[1])
        rank = 1/float(udg.order())
        nx.set_node_attributes(udg, 'rank', rank)
        return udg


def read_demo_data(datafilename, isDirected):
    with open(datafilename, 'r') as fin:
        creader = csv.reader(fin, delimiter=',')
        data = [row for row in creader]
    fin.close()
    print "Reading data and building graph ... "
    if isDirected:
        return build_directed_graph(data)
    else:
        return build_undirected_graph(data)


def build_directed_graph(data):
    dg = nx.DiGraph() # directed graph
    for entry in data:
        node_dst = entry[0].strip().strip('"')
        val_dst = digits(entry[1])
        node_src = entry[2].strip().strip('"')
        val_src = digits(entry[3])
        edge_weight = val_dst - val_src
        if edge_weight >= 0:
            dg.add_edge(node_src, node_dst, weight=1)
        else:
            dg.add_edge(node_dst, node_src, weight=1)
    return dg


def build_undirected_graph(data):
    udg = nx.Graph()
    edges = [(entry[0], entry[2]) for entry in data]
    nodes = [entry[0] for entry in data]
    nodes.extend([entry[2] for entry in data])
    rank = 1/float(len(set(nodes)))
    udg.add_nodes_from(nodes, rank=rank)
    udg.add_edges_from(edges, weight=1)
    return udg


def digits(val):
    return int(re.sub("\D", "", val))