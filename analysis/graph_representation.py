class GraphNode:

    def __init__(self, node_id, node_type, features=None):
        self.id = node_id
        self.type = node_type
        self.features = features or {}


class GraphEdge:

    def __init__(self, source, target, edge_type):
        self.source = source
        self.target = target
        self.type = edge_type


class ProgramGraph:

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.node_counter = 0

    def new_node(self, node_type, features=None):
        node_id = self.node_counter
        self.node_counter += 1

        node = GraphNode(node_id, node_type, features)
        self.nodes[node_id] = node
        return node_id

    def add_edge(self, src, dst, edge_type):
        self.edges.append(GraphEdge(src, dst, edge_type))