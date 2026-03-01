def extract_critical_subgraph(pdg, graph_data):

    important_nodes = []

    for edge in pdg.edges:
        if edge.type == "DATA_DEP":
            important_nodes.append(edge.source)
            important_nodes.append(edge.target)

    return list(set(important_nodes))