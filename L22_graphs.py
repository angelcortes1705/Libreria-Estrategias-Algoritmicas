from enum import Enum
from functools import total_ordering
from typing_extensions import Self
from collections import deque, defaultdict

class NodeColor(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2

@total_ordering
class Node:
    def __init__(self, value: int):
        self.value = value
        self.color = NodeColor.WHITE
        self.distance = float("inf")
        self.discovered = float("inf")
        self.finished = float("inf")
        self.parent: Node = None
    def __repr__(self) -> str:
        return str(self.value)
    def __lt__(self, other) -> bool:
        return self.value < other.value
    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.value == other.value
    def __hash__(self) -> int:
        return hash(self.value)

class GraphType(Enum):
    UNDIRECTED = 0
    DIRECTED = 1

class Graph:
    def __init__(self, type_: GraphType):
        self.type = type_
        self.V: dict[int, Node] = dict()
        self.E: set[tuple[Node, Node]] = set()
        self.Adj: dict[Node, set[Node]] = dict()

    def __repr__(self):
        return str(self.Adj)

    def get_node(self, s: int) -> Node:
        return self.V.get(s, None)

    def add_node(self, v: int):
        v_node = self.get_node(v)
        if not v_node:
            v_node = Node(v)
            self.V[v] = v_node
            self.Adj[v_node] = set()

    def add_edge(self, u: int, v: int):
        u = self.get_node(u)
        v = self.get_node(v)
        if u and v:
            self.E.add((u, v))
            self.Adj[u].add(v)
            if self.type == GraphType.UNDIRECTED:
                self.Adj[v].add(u)
        else:
            raise ValueError("Node not found in graph")

    def add_nodes(self, v_list: list[int]):
        for v in v_list:
            self.add_node(v)

    def add_edges(self, e_list: list[tuple[int, int]]):
        for e in e_list:
            self.add_edge(*e)

    def __reset_nodes(self):
        for v in self.V.values():
            v.color = NodeColor.WHITE
            v.distance = float("inf")
            v.discovered = float("inf")
            v.finished = float("inf")
            v.parent = None

    def bfs(self, s: int) -> Node:
        self.__reset_nodes()
        s = self.get_node(s)
        s.color = NodeColor.GRAY
        s.distance = 0
        s.parent = None
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in self.Adj[u]:
                if v.color == NodeColor.WHITE:
                    v.color = NodeColor.GRAY
                    v.distance = u.distance + 1
                    v.parent = u
                    queue.append(v)
            u.color = NodeColor.BLACK
        return s

    def get_bft(self, s: int) -> Self:
        self.bfs(s)
        bft = Graph(GraphType.DIRECTED)
        bft.add_nodes(list(self.V.keys()))
        for v in self.V.values():
            if v.parent:
                bft.add_edge(v.parent.value, v.value)
        return bft

    def print_path(self, s: int, v: int) -> list[int]:
        path = []
        s = self.get_node(s)
        v = self.get_node(v)
        if v == s:
            return [s.value]
        if v.parent is None:
            return []
        while v != s:
            path.append(v.value)
            v = v.parent
        path.append(s.value)
        return path[::-1]

    def dfs(self):
        self.__reset_nodes()
        self.time = 0
        for u in sorted(self.V.values(), key=lambda x: x.value):
            if u.color == NodeColor.WHITE:
                self.__dfs_visit(u)

    def __dfs_visit(self, u: Node):
        self.time += 1
        u.discovered = self.time
        u.color = NodeColor.GRAY
        for v in self.Adj[u]:
            if v.color == NodeColor.WHITE:
                v.parent = u
                self.__dfs_visit(v)
        u.color = NodeColor.BLACK
        self.time += 1
        u.finished = self.time

    def __classify_edges(self) -> dict[str, list[tuple]]:
        edge_types = {"tree": [], "back": [], "forward": [], "cross": []}
        self.dfs()
        for u in self.V.values():
            for v in self.Adj[u]:
                if v.parent == u:
                    edge_types["tree"].append((u, v))
                elif v.color == NodeColor.GRAY:
                    edge_types["back"].append((u, v))
                elif u.discovered < v.discovered:
                    edge_types["forward"].append((u, v))
                else:
                    edge_types["cross"].append((u, v))
        return {k: [(u.value, v.value) for u, v in vlist] for k, vlist in edge_types.items()}

    def topological_sort(self) -> list[int]:
        self.__classify_edges()
        for u in self.V.values():
            for v in self.Adj[u]:
                if u.discovered < v.discovered < u.finished < v.finished:
                    raise TypeError("Topological sort is not defined for cyclic graphs.")
        return [v.value for v in sorted(self.V.values(), key=lambda x: -x.finished)]

    def scc(self) -> list[list[int]]:
        def reverse_graph():
            gr = Graph(GraphType.DIRECTED)
            gr.add_nodes(list(self.V.keys()))
            for u in self.Adj:
                for v in self.Adj[u]:
                    gr.add_edge(v.value, u.value)
            return gr

        self.dfs()
        order = sorted(self.V.values(), key=lambda x: -x.finished)
        GT = reverse_graph()
        GT.__reset_nodes()
        result = []

        def dfs_collect(u, component):
            u.color = NodeColor.GRAY
            component.append(u.value)
            for v in GT.Adj[u]:
                if v.color == NodeColor.WHITE:
                    dfs_collect(v, component)
            u.color = NodeColor.BLACK

        for u in order:
            node = GT.get_node(u.value)
            if node.color == NodeColor.WHITE:
                component = []
                dfs_collect(node, component)
                result.append(component)
        return result



if __name__ == "__main__":
    G = Graph(GraphType.DIRECTED)
    G.add_nodes(list("abcdefgh"))
    G.add_edges(
        [
            ("a", "b"),
            ("b", "c"),
            ("b", "e"),
            ("b", "f"),
            ("c", "d"),
            ("c", "g"),
            ("d", "c"),
            ("d", "h"),
            ("e", "a"),
            ("e", "f"),
            ("f", "g"),
            ("g", "f"),
            ("g", "h"),
            ("h", "h"),
        ]
    )

    print(G.Adj)
    # {a: {b}, b: {c, f, e}, c: {d, g}, d: {h, c}, e: {f, a}, f: {g}, g: {h, f}, h: {h}}

    G.bfs("a")
    for v in G.V.values():
        print(v, v.distance, v.parent)
    # a 0 None
    # b 1 a
    # c 2 b
    # d 3 c
    # e 2 b
    # f 2 b
    # g 3 c
    # h 4 g

    bft = G.get_bft("a")
    print(bft)
    # {g: {h}, f: {g}, a: {b}, h: set(), e: set(), d: set(), b: {c, f, e}, c: {d}}

    print(G.print_path("a", "h"))
    # ['a', 'b', 'c', 'g', 'h']

    G.dfs()
    for v in G.V.values():
        print(v.value, v.parent, v.discovered, v.finished)
    # a None 1 16
    # b a 2 15
    # c b 11 14
    # d c 12 13
    # e b 3 10
    # f e 4 9
    # g f 5 8
    # h g 6 7

    try:
        print(G.topological_sort())
        # TypeError: Topological sort is not defined for cyclic graphs.
    except:
        pass

    print(G._Graph__classify_edges())
    # {'tree': [(a, b), (b, f), (b, c), (b, e), (c, d), (f, g), (g, h)],
    #  'back': [(d, c), (e, a), (g, f), (h, h)],
    #  'forward': [],
    #  'cross': [(c, g), (d, h), (e, f)]}

    print(G.scc())
    # [['b', 'e', 'a'], ['d', 'c'], ['g', 'f'], ['h']]
