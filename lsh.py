#!/usr/bin/python

'''
This class implements Locality Sensitivity Hashing 

Reference: Textbook Chapter 3.3 Pages 84 and 85

'''

import numpy as np
import pandas as pd
import random
from sklearn.metrics import jaccard_similarity_score

def construct_permutations():
	'''
	This function constructs a permuation matrix with 100 permutations
	It stores it in the hadoop file system for reading later
	'''
	num_permutations = 100
	num_cols = 33	# 29 flight data cols + 4 weather cols
	hash_matrix = []
	
	for i in xrange(num_permutations): 
		hash_matrix.append(np.random.permutation(num_cols))
	
	hash_matrix = np.array(hash_matrix)
	df = pd.DataFrame(hash_matrix)
	df.to_csv('hash.csv', header=None, index=False)

class lsh:
	def __init__(self, dataframe):
		print "Initialising LSH"
		
		self.dataframe = dataframe
		self.dataframe_cols = len(self.dataframe.axes[1])
		self.dataframe_rows = len(self.dataframe.axes[0])
		self.transformed_dataframe = None
		self.hash_matrix = []
		self.signature_matrix = np.zeros((self.num_permutations, self.dataframe_rows))
		
	def create_lsh(self):
		self.hash_dataframe()
		
		# For testing
		# print self.query(self.dataframe.iloc[1]) 
		
	def hash_dataframe(self):
		self.transformed_dataframe = self.dataframe.applymap(self.transform_binary) 
		self.construct_signature_matrix()
	
	def transform_binary(self, val):
		'''
		This function does a simple transformation of numbers to binary string
		1. If number < 0, replace negative sign with '9'
		2. Remove decimal points
		3. Count the number of digits > 5 in number
		4. If count > 3, return 1; else return 0 (small numbers)
		Note: Need to tweak this number 
		TODO: Make bytes
		'''
		val = str(val)
		# Replace negative signs
		val = val.replace('-', '9')
		# Remove decimal points
		val = ''.join(ch for ch in str(val) if ch.isdigit())		
		greater_five = len(filter(lambda x: int(x) > 5, val))
		
		return 1 if greater_five > 3 else 0
	
	def construct_signature_matrix(self):
		#matrix_transpose = np.matrix(self.hash_matrix).transpose()
		#self.matrix_array = np.array(matrix_transpose)
		self.matrix_array = np.array(self.hash_matrix)

		for idx, row in self.transformed_dataframe.iterrows():
			for i in xrange(self.num_permutations):
				permutations = self.matrix_array[i]
				for perm_idx in permutations: 
					# print str(perm_idx) + " " + str(row[perm_idx])
					if row[perm_idx] == 1:
						self.signature_matrix[i][idx] = perm_idx
						break
					else:
						continue

	
	def query(self, query_vector, num_neighbours=200):
		'''
		Input: query_vector as row from dataframe
		Returns np.array of row numbers of top num_neighbours rows
		TODO: Banding/ map-reduce
		'''
		# Permutate the query vector
		query_transformed_vector = query_vector.apply(self.transform_binary)
		query_perm_vector = []
		# print "Transformed vector"
		# print query_transformed_vector
		# print str(len(query_transformed_vector))

		for i in xrange(len(self.matrix_array)):
			permutation = self.matrix_array[i]
			for perm_idx in permutation:
				if query_transformed_vector[perm_idx] == 1:
					query_perm_vector.append(perm_idx)
					break
				else:
					continue
		
		print "Permutated Vector"
		# print query_perm_vector
		
		# Just in case length is 0 - quick hack for the moment 
		if len(query_perm_vector) == 0 :
			query_perm_vector = [0] * self.num_permutations
		
		similarity = []
		self.matrix_array = np.array(self.signature_matrix)
		for col in self.signature_matrix.T:
			similarity.append(self.jaccard_similarity(query_perm_vector, col))
		
		# Row numbers of top num_neighbours similar rows
		idx = (-np.array(similarity)).argsort()[:num_neighbours]
		return idx
		
	def jaccard_similarity(self, query_vector, vector):
		return jaccard_similarity_score(query_vector, vector)
	
		