import networkx as nx
import numpy as np
from numpy.random import RandomState
import itertools

float_formatter = "{:.2f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})
np.set_printoptions(precision=2)

SEED=0
np_random_generator = RandomState(SEED)

# Params setup
KGs=["BASE","DENSE","SUPERDENSE"]
ps=[0.2, 0.5, 0.7]
nodes=[100,250,500,1000]

params = list(itertools.product(zip(KGs, ps),nodes))
for i in range(len(params)):
    params[i] = tuple(itertools.chain(params[i][0],[params[i][1]]))
    
# graphs generation   
for KG, p, nodes in params:
    G = nx.DiGraph(nx.fast_gnp_random_graph(n=nodes, p=p).edges())
    for node in G.nodes():
        incoming_edges: int = len(G.in_edges(node))
        if incoming_edges == 0:
            continue
        shares = np_random_generator.randint(low=1, high=100, size=incoming_edges)
        shares = shares / shares.sum()
        assert len(shares)>0
        for edge, share in zip(G.in_edges(node), shares):
            assert node==edge[1]
            if share > 0.9999:
                assert incoming_edges==1
            else: 
                assert incoming_edges>1
            G[edge[0]][edge[1]]['share'] = share
    print(f"n={nodes} p={p} edges={len(G.edges())} d={nx.density(G)}")
    adj_matrix=nx.adjacency_matrix(G, weight='share').todense()
    np.savetxt(f"graph_{KG}_n={nodes}_p={p}.csv", adj_matrix, delimiter=",", fmt="%1.2f")