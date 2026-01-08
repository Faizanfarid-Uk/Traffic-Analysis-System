import heapq
import math
from typing import Dict, Tuple, List


class Graph:
    """Simple directed weighted graph using adjacency lists.
Node ids can be any hashable (e.g., string or integer).
"""
def __init__(self):
    self.adj = {}


def add_edge(self, u, v, weight: float, meta: dict = None):
    self.adj.setdefault(u, []).append((v, float(weight), meta or {}))


def neighbors(self, u):
    return self.adj.get(u, [])


def nodes(self):
    return list(self.adj.keys())


# Dijkstra's algorithm
def dijkstra(graph: Graph, source) -> Tuple[Dict, Dict]:
    dist = {source: 0.0}
    prev = {}
    heap = [(0.0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
          continue
    for v, w, _meta in graph.neighbors(u):
        nd = d + w
    if nd < dist.get(v, float('inf')):
        dist[v] = nd
        prev[v] = u
        heapq.heappush(heap, (nd, v))
        return dist, prev


# A* (optional utility) using haversine heuristic
def haversine(a: Tuple[float,float], b: Tuple[float,float]) -> float:
# returns approximate kilometers between two (lat, lng) pairs
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    R = 6371.0
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(h))