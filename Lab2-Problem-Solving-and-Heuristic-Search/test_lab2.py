import csv
import heapq
import math
import unittest
from collections import deque
from pathlib import Path

HERE = Path(__file__).parent

def load_graph_and_h():
    graph = {}
    edges_file = HERE / "synthetic_route_edges.csv"
    for row in csv.DictReader(open(edges_file, newline="", encoding="utf-8")):
        graph.setdefault(row["source"], []).append((row["destination"], float(row["cost_units"])))
    for _, edges in list(graph.items()):
        for v, _ in edges: graph.setdefault(v, [])
    for u in graph: graph[u] = sorted(graph[u], key=lambda e: e[0])

    heuristics_file = HERE / "synthetic_heuristics.csv"
    h = {r["node"]: float(r["heuristic_remaining_cost"])
         for r in csv.DictReader(open(heuristics_file, newline="", encoding="utf-8"))}
    return graph, h

def path_cost(graph, path):
    if path is None: return math.inf
    return sum(dict(graph[u])[v] for u, v in zip(path, path[1:]))

def bfs(graph, start="S", goal="G"):
    if start == goal: return [start], 0.0, [start]
    discovered = {start: None}
    queue = deque([start])
    expanded = []
    while queue:
        u = queue.popleft()
        expanded.append(u)
        if u == goal:
            path = []
            curr = u
            while curr is not None:
                path.append(curr)
                curr = discovered[curr]
            path.reverse()
            return path, path_cost(graph, path), expanded
        for v, _ in graph.get(u, []):
            if v not in discovered:
                discovered[v] = u
                queue.append(v)
    return None, math.inf, expanded

def best_first(graph, h, start="S", goal="G", mode="ucs"):
    for u in graph:
        for v, cost in graph[u]:
            if cost < 0: raise ValueError(f"Negative cost ({u}, {v})")
    best_g = {start: 0.0}
    parent = {start: None}
    
    def make_priority(node, g_val):
        h_val = h.get(node, 0.0)
        if mode == "ucs": return (g_val, node)
        elif mode == "greedy": return (h_val, node)
        elif mode == "astar": return (g_val + h_val, h_val, node)
        raise ValueError(f"Unknown mode: {mode}")

    heap = []
    prio = make_priority(start, 0.0)
    heapq.heappush(heap, (*prio, start, 0.0))
    expanded = []
    closed = set()
    
    while heap:
        item = heapq.heappop(heap)
        node = item[-2]
        stored_g = item[-1]
        if stored_g > best_g[node]: continue
        if mode == "greedy":
            if node in closed: continue
            closed.add(node)
        expanded.append(node)
        if node == goal:
            path = []
            curr = node
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path, path_cost(graph, path), expanded
        for v, cost in graph.get(node, []):
            cand_g = stored_g + cost
            if cand_g < best_g.get(v, math.inf):
                best_g[v] = cand_g
                parent[v] = node
                prio_v = make_priority(v, cand_g)
                heapq.heappush(heap, (*prio_v, v, cand_g))
    return None, math.inf, expanded

def consistency_violations(graph, h, goal="G"):
    violations = []
    if h.get(goal, 0.0) != 0.0: violations.append(("GOAL_CHECK", goal, h.get(goal)))
    for u in sorted(graph):
        for v, cost in graph[u]:
            if h.get(u, 0.0) > cost + h.get(v, 0.0):
                violations.append((u, v, cost))
    return violations

class TestLab2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph, cls.h = load_graph_and_h()

    def test_bfs(self):
        path, cost, exp = bfs(self.graph)
        self.assertEqual(path, ["S", "A", "C", "G"])
        self.assertEqual(cost, 14.0)
        self.assertEqual(exp, ["S", "A", "B", "C", "D", "E", "G"])

    def test_ucs(self):
        path, cost, exp = best_first(self.graph, self.h, mode="ucs")
        self.assertEqual(path, ["S", "B", "D", "E", "G"])
        self.assertEqual(cost, 9.0)
        self.assertEqual(exp, ["S", "A", "B", "C", "D", "E", "G"])

    def test_greedy(self):
        path, cost, exp = best_first(self.graph, self.h, mode="greedy")
        self.assertEqual(path, ["S", "B", "E", "G"])
        self.assertEqual(cost, 11.0)
        self.assertEqual(exp, ["S", "B", "E", "G"])

    def test_astar(self):
        path, cost, exp = best_first(self.graph, self.h, mode="astar")
        self.assertEqual(path, ["S", "B", "D", "E", "G"])
        self.assertEqual(cost, 9.0)
        self.assertEqual(exp, ["S", "B", "D", "E", "G"])

    def test_consistency(self):
        self.assertEqual(consistency_violations(self.graph, self.h), [])
        bad_h = dict(self.h)
        bad_h["B"] = 7.0
        violations = consistency_violations(self.graph, bad_h)
        self.assertEqual(violations, [("B", "D", 1.0)])

if __name__ == "__main__":
    unittest.main()
