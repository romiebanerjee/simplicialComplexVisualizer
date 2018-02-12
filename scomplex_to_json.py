
import numpy as np
import pandas as pd 
import json

#==============================================================

def flatten(A):
	if A == []: return A
	if type(A[0]) == list:
		return flatten(A[0]) + flatten(A[1:])
	else: return [A[0]] + flatten(A[1:])

#===========================================================================================================

class scomplex():
	def __init__(self, simplices = []):
		self.simplices = list(set(flatten([self.simplexfaces(simplex) for simplex in simplices])))
		self.vertices = [simplex for simplex in self.simplices if len(simplex)-1 == 0]
		self.dim = max(len(x)-1 for x in self.simplices)
		self.topdimsimplices = [simplex for simplex in self.simplices if len(simplex)-1 == self.dim]
		self.topsimplices = self.topdimsimplices  
		self.facetree = self.facetree()

	def Sigma(self,k):
		return [simplex for simplex in self.simplices if len(simplex)-1 == k]
	
	def d(self,simplex,i):
		if i in range(len(simplex)):
			return simplex[0:i] + simplex[i+1:len(simplex)]
		else:pass

	def simplextree(self, simplex):
		simplextree = []
		if len(simplex) == 1: return [simplex,[]]
		else:
			simplextree = [simplex]
			for i in range(len(simplex)):
				simplextree.append(self.simplextree(self.d(simplex,i)))
		return simplextree
	

	def simplexfaces(self,simplex):
		return flatten(self.simplextree(simplex))


	def facetree(self):
		return [self.simplextree(simplex) for simplex in self.topsimplices]	

	def D(self,k):
		if k in range(self.dim +1):
			if k == 0: return np.zeros(len(self.Sigma(0)))
			else:
				n = len(self.Sigma(k))
				m = len(self.Sigma(k-1))
				A = np.zeros((m,n))
				for i in range(m):
					for j in range(n):
						for l in range(k+1):
							if self.Sigma(k-1)[i] == self.d(self.Sigma(k)[j],l):
								A[i,j] = (-1)**l
							else: pass
				return A
		elif k == self.dim+1: return np.zeros((1,1))	
		else: pass


	def betti(self):
		return [len(self.Sigma(k)) - np.linalg.matrix_rank(self.D(k)) - np.linalg.matrix_rank(self.D(k+1)) for k in range(self.dim +1)]

#=============================================================================================================================


def make_json(complex):

    Z = scomplex(simplices = complex)

    V = Z.Sigma(0)
    E = Z.Sigma(1)
    F = Z.Sigma(2)

    nodes = [{"id": v} for v in V]
    edges = [{"source": V.index(link[0]), "target": V.index(link[1])} for link in E]
    faces = [[{"node": V.index(node[0]) }, {"node": V.index(node[1])}, {"node": V.index(node[2])}] for node in F]

        
    scomplex_data = {"nodes":nodes, "edges": edges, "faces": faces}

    json_data = json.dumps(scomplex_data)

    file = open("scomplex_data.json", 'w')
    file.write(json_data)
    file.close()




