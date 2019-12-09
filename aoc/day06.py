import networkx as nx


def solve(file, verbose):
    di_graph = nx.parse_edgelist(file, delimiter=')', create_using=nx.DiGraph)

    root, = (n for n,d in di_graph.in_degree() if d == 0)
    path_lengths = nx.single_source_shortest_path_length(di_graph, source=root)
    print('Part 1:', sum(path_lengths.values()))

    graph = di_graph.to_undirected(as_view=True)
    our_parent, = graph.neighbors('YOU')
    san_parent, = graph.neighbors('SAN')

    path_length = nx.shortest_path_length(graph, target=san_parent, source=our_parent)

    print('Part 2:', path_length)
