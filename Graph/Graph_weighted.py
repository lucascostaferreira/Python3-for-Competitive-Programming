"""
Weighted Graph
"""

class Node(object):

	def __init__(self, idf, weight=False):
		self.idf = idf
		self.weight = weight
		self.edges = dict()

class Graph(object):

	def __init__(self, nodes=[], directed=False):
		self._nodes = { idf:Node(idf,weight) for idf,weight in nodes }
		self._directed = directed

	def get_node(self, idf):
		return self._nodes[idf]

	def add_edge(self, u, v, weight=0):
		self._nodes[u].edges[v] = weight
		if not self._directed:
			self._nodes[v].edges[u] = weight

	def del_edge(self, u, v):
		self._nodes[u].edges.pop(v)
		if not self._directed:
			self._nodes[v].edges.pop(u)