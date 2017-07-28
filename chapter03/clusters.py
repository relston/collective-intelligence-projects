def readfile(filename):
	lines = [line for line in file(filename)]

	# Getting the column titles from the first line
	colnames = lines[0].strip().split('\t')[1:] #slice syntax [start index : end index : increment]
	rownames = []
	data = []
	for line in lines[1:]:
		# break out line into array of cells
		p = line.strip().split('\t')
		# first cell is the row name
		rownames.append(p[0])
		# rest is the data which get put into a matrix (array of arrays)
		data.append([float(x) for x in p[1:]]) #slice syntax is everywhere
	return (rownames, colnames, data)

from math import sqrt

#two vectors (or lists) - compare 
def pearson(v1, v2):
	# Simple sums
	sum1 = sum(v1)
	sum2 = sum(v2)

	# Sums of the squares
	sum1Sq = sum([pow(v, 2) for v in v1])
	sum2Sq = sum([pow(v, 2) for v in v2])

	# Sum of the products
	pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

	# Calculate r (Pearson score)
	num = pSum - sum1 * sum2 / len(v1)
	den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
	if den == 0:
		return 0
	return 1.0 - num / den

# creating a class to hold the grouping information 
class bicluster:
	def __init__( self, vec, left=None, right=None, distance=0.0, id=None ):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance

def hcluster(rows, distance=pearson):
	distances = {}
	currentclustid = -1

	# Clusters are initially just the rows
	clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

	while len(clust) > 1:
		lowestpair = (0, 1)
		
		print  'comparing vec of length  %s  to a vec of length %s' % (len(clust[0].vec), len(clust[1].vec))
		closest = distance(clust[0].vec, clust[1].vec)

		# loop through every pair looking for the smallest distance
		for i in range(len(clust)):
			for j in range(i + 1, len(clust)): # what kind of sort is this? 
				# always do a compare from the next one becase all the previous items have been compaired already. billiant.
				# distances is the cache of distance calculations
				if (clust[i].id, clust[j].id) not in distances: 
					distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

				d = distances[(clust[i].id, clust[j].id)]

				if d < closest:
					closest = d
					lowestpair = (i, j)

		# calculate the average of the two clusters
		# loop through all the words in the vector and get the average number between the two closest clusters
		mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]

		# create the new cluster
		newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
							   right=clust[lowestpair[1]], distance=closest,
							   id=currentclustid)

		# cluster ids that weren't in the original set are negative
		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)

	return clust[0]

def printclust(clust, labels=None, n=0):
	# indent to make a hierarchy layout
	for i in range(n):
		print ' ',
	if clust.id < 0:
	# negative id means that this is branch
		print '-'
	else:
	# positive id means that this is an endpoint
		if labels == None:
			print clust.id
		else:
			print labels[clust.id]
	# now print the right and left branches
	if clust.left != None:
		printclust(clust.left, labels=labels, n=n + 1)
	if clust.right != None:
		printclust(clust.right, labels=labels, n=n + 1)