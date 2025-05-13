import random
from enum import Enum
from itertools import combinations
from functools import total_ordering
import heapq

class NodeColor(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2

@total_ordering
class Node:
    def __init__(self, value: int):
        self.value = value
        self.color = NodeColor.WHITE
        self.discovered = float("inf")
        self.finished = float("inf")
        self.d = float("inf")
        self.parent: Node = None

    def __repr__(self) -> str:
        return str(self.value)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        if other is None:
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
        self.E: dict[tuple[Node, Node], float] = dict()
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

    def add_edge(self, u: int, v: int, w: float):
        u = self.get_node(u)
        v = self.get_node(v)
        if u and v:
            self.E[(u, v)] = w
            self.Adj[u].add(v)
            if self.type == GraphType.UNDIRECTED:
                self.Adj[v].add(u)
        else:
            raise ValueError("Node not found in graph")

    def add_nodes(self, v_list: list[int]):
        for v in v_list:
            self.add_node(v)

    def add_edges(self, e_list: list[tuple[int, int, float]]):
        for e in e_list:
            self.add_edge(*e)

    def __reset_nodes(self):
        for v in self.V.values():
            v.color = NodeColor.WHITE
            v.discovered = float("inf")
            v.finished = float("inf")
            v.d = float("inf")
            v.parent = None

    def w(self, u: Node, v: Node) -> float:
        if not isinstance(u, Node):
            u = self.get_node(u)
        if not isinstance(v, Node):
            v = self.get_node(v)
        return self.E.get((u, v), None)

    def __relax(self, u: Node, v: Node) -> bool:
        w_uv = self.w(u, v)
        if v.d > u.d + w_uv:
            v.d = u.d + w_uv
            v.parent = u
            return True
        return False

    def bellman_ford(self, s: int) -> bool:
        self.__reset_nodes()
        s = self.get_node(s)
        s.d = 0

        for _ in range(len(self.V) - 1):
            for (u, v), w in self.E.items():
                self.__relax(u, v)

        # Revisión de ciclos negativos
        for (u, v), w in self.E.items():
            if v.d > u.d + w:
                return False
        return True

    def __dfs_visit(self, u: Node, time: list, stack: list[Node]):
        time[0] += 1
        u.discovered = time[0]
        u.color = NodeColor.GRAY

        for v in self.Adj[u]:
            if v.color == NodeColor.WHITE:
                v.parent = u
                self.__dfs_visit(v, time, stack)

        u.color = NodeColor.BLACK
        time[0] += 1
        u.finished = time[0]
        stack.append(u)

    def __dfs(self) -> list[Node]:
        self.__reset_nodes()
        time = [0]
        stack = []
        for u in sorted(self.V.values(), key=lambda x: x.value):
            if u.color == NodeColor.WHITE:
                self.__dfs_visit(u, time, stack)
        return stack[::-1]  # topological sort

    def dags(self, s: int):
        self.__reset_nodes()
        s = self.get_node(s)
        sorted_nodes = self.__dfs()
        s.d = 0

        for u in sorted_nodes:
            for v in self.Adj[u]:
                self.__relax(u, v)

    def dijkstra(self, s: int):
        self.__reset_nodes()
        s = self.get_node(s)
        s.d = 0
        Q = list(self.V.values())
        heap = [(v.d, v) for v in Q]
        heapq.heapify(heap)

        while heap:
            _, u = heapq.heappop(heap)
            for v in self.Adj[u]:
                if self.__relax(u, v):
                    heapq.heappush(heap, (v.d, v))

    def print_path(self, s: int, v: int) -> list[tuple[int, float]]:
        s = self.get_node(s)
        v = self.get_node(v)
        path = []

        while v != s:
            if v is None:
                return []
            path.append((v.value, v.d))
            v = v.parent

        path.append((s.value, s.d))
        return path[::-1]

    def bellman_ford_shortest_paths(self, s: Node, v: Node) -> list[tuple[int, float]]:
        if self.bellman_ford(s):
            return self.print_path(s, v)
        raise ValueError("Negative weight cycle found in Graph.")

    def dags_shortest_paths(self, s: Node, v: Node) -> list[tuple[int, float]]:
        self.dags(s)
        return self.print_path(s, v)

    def dijkstra_shortest_paths(self, s: Node, v: Node) -> list[tuple[int, float]]:
        self.dijkstra(s)
        return self.print_path(s, v)

if __name__ == "__main__":
    G = Graph(GraphType.DIRECTED)
    nodes = range(20)
    G.add_nodes(nodes)
    edges = [(i, j, random.random()) for i, j in combinations(nodes, 2)]
    random.shuffle(edges)
    edges = edges[:50]
    G.add_edges(edges)

    # Usa índices, no nodos
    bellman_path = G.bellman_ford_shortest_paths(0, 18)
    dijkstra_path = G.dijkstra_shortest_paths(0, 18)
    dags_path = G.dags_shortest_paths(0, 18)

    assert bellman_path == dijkstra_path == dags_path
    print("All algorithms returned the same shortest path.")

