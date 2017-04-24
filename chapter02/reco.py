# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener' : 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

import logging
from math import sqrt
#setting up logging 
logging.basicConfig(level=logging.DEBUG)


# Get the distance-based (Euclidean) similarity score for person 1 and person 2 (p1, p2)
def getDistance(prefs, p1, p2):
	#find shared items in preferences
	sPrefs={}
	for item in prefs[p1]:
		if item in prefs[p2]: sPrefs[item]=1
	#why set it to 1?

	#nothing in common? return 0
	if len(sPrefs)==0: return 0

	#adding the sum of squares of the distances
	for item in prefs[p1]:
		if item in prefs[p2]:
			# doing some logging just so I can take in the numbers
			eDist=pow(prefs[p1][item] - prefs[p2][item], 2)
			iDist=1/(1+eDist)
			
	sumOfSquares = sum([pow(prefs[p1][item] - prefs[p2][item], 2)
			for item in prefs[p1] if item in prefs[p2]])
	invSum = 1/(1+sumOfSquares)

	return invSum

#getDistance(critics, 'Lisa Rose', 'Gene Seymour')
# 0.148148148148 not sure how thats helpful just yet

def getPearson(prefs,p1,p2):
	#find shared items in preferences
	sPrefs={}
	for item in prefs[p1]:
		if item in prefs[p2]: sPrefs[item]=1
	#nothing in common? return 0
	if len(sPrefs)==0: return 0

	# \length of calculaions
	n=len(sPrefs)
	#logging.debug("length of calc: %s" % n)

	#some of all the preferences
	sum1=sum([prefs[p1][it] for it in sPrefs])
	sum2=sum([prefs[p2][it] for it in sPrefs])
	#logging.debug("Sums for %s: %s" % (p1, sum1))
	#logging.debug("Sums for %s: %s" % (p2, sum2))
	#seems like we are getting relative scales?

	#sum the squares of the prefs
	sum1Sq=sum([pow(prefs[p1][it],2) for it in sPrefs])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in sPrefs])	
	#logging.debug("Sqr Sum for %s: %s" % (p1, sum1Sq))
	#logging.debug("Sqr Sum for %s: %s" % (p2, sum2Sq))

	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in sPrefs])
	#logging.debug("Sum of product: %s" % pSum)	
	#so now we are mutiplying eche of the movie pref together and getting the some of those?
	#looks like a number btween the indevidual sum squares
	
	#Calculate r (Pearson score)
	num=pSum-(sum1*sum2/n)
	#logging.debug("Number 1: %s" % num)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	#logging.debug("den: %s" % den)
	if den==0: return 0

	r=num/den
	#logging.debug("person score: %s" % r)

	#so it seems the main difference is that Person scores range from -1 to 1 
	# oh thats right its a vector, if its negitive 
	# the more somone might like something the less the other might
	# divergent opinions?
	return r	
# this both seem to give pretty similar results in practice, 
# I guess the author felt he really needed to highlight that 
# theres didferent ways to calculate the same sort of thing


#getPearson(critics, 'Lisa Rose', 'Gene Seymour')

#given one person, rank the other by similarity
def topMatches(prefs,user,n=5,similarity=getPearson):
	scores=[(similarity(prefs,user,other),other) 
		for other in prefs if other!=user]
	scores.sort()
	scores.reverse()
	return scores[0:n]

#logging.debug("Results: %s" % topMatches(critics, 'Lisa Rose'))

#get recos by a weighted average other peoples user rankings based on similarity
def getRecommendations(prefs, person, similarity=getPearson):
	totals={}
	simSums={}
	for other in prefs:
		if other==person: continue
		#get that score to we can weight it
		sim=similarity(prefs, person, other)
		#ignore low similairy people, what do they know anyway?
		if sim<=0: continue

		for item in prefs[other]: #get those movies
			
			#only score new movies that I havent seen
			if item not in prefs[person] or prefs[person][item]==0:
				#building a sum of all the similarity-weighted scores from everyone by item
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				#...and just build sum of all the similarity muitpliers we used for this item
				simSums.setdefault(item,0)
				simSums[item]+=sim
	# this is gonna take the sum total weighted score for a each movie
	# ...and return a "normalized list" 
	# where the keys are the final scores for the film
	# and the values are the film names
	rankings=[(total/simSums[item], item) for item,total in totals.items()]

	rankings.sort() #guess this is gonna sort the keys (scores), asc
	rankings.reverse() #key order will now be large to small, desc
	return rankings

logging.debug("Results: %s" % getRecommendations(critics, 'Toby', getDistance))
logging.debug("Results: %s" % getRecommendations(critics, 'Toby', getPearson))

def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})

			# Flip item and person
			result[item][person]=prefs[person][item]
	return result

movies=transformPrefs(critics)
# people who liked this movie also liked...
logging.debug("Recomend Movies: %s" % topMatches(movies, 'Superman Returns'))
# get recommended critics for a given movie? oh yeah critics that havent seen the movie ranked by similarity
# thats a weird one...
logging.debug("Recoment Critics: %s" % getRecommendations(movies, 'Lady in the Water'))
