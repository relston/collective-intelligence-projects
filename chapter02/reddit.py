import logging
import praw
from math import sqrt
#setting up logging 
logging.basicConfig(level=logging.DEBUG)

reddit = praw.Reddit(client_id='5N8DrwZWCo7LIA', client_secret='y17XLY7YIiWEQ3xSptUSLOeZ9U8', user_agent='testscript by /u/ryanelston')
#logging.debug("Results: %s" % reddit)

#frontpage={}
#for submission in reddit.front.hot():
	#logging.debug("Post: %s" % submission.title)#__dict__.items())# 	shortlink)#.shortlink)
## im sure this is more of the same recomendaiton scheem 

def initializeUserDict(count=20):
	user_dict={}
	#get the top popular post on the front page
	for topPost in reddit.front.top(limit=count):
		#find all user that posted this
		url = topPost.url
		#get eveyone who also posted this
		for dupPost in topPost.duplicates():
			user_dict[dupPost.author]={}
			return user_dict

logging.debug(initializeUserDict())

def fillItems(user_dict):
	all_items={}
	# Find links posted by all users
	logging.debug("filling items")
	for user in user_dict:	
		try:
			#posts=get_userposts(user)
			posts=user.upvoted(limit=5)
			logging.debug(posts)
			break
		except:
			print "Failed user "
			break
		try:
			for post in posts:
				user_dict[user][post]=post.ups
				all_items[post]=post.ups
		except:
			print "WTF fail posts"

	# Fill in missing items with 0
	for ratings in user_dict.values():
		for item in all_items:
			if item not in ratings:
				ratings[item]=0.0

logging.debug(fillItems(initializeUserDict()))