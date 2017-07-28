import feedparser
import re

def getWordCount(url):
	print 'Getting '+url
	feed=feedparser.parse(url)
	wordCount={}
	for entry in feed.entries:
		if 'summary' in entry: summary=entry.summary
		else: summary=entry.description

		#get those words
		words=getWords(entry.title+' '+summary)
		for word in words:
			wordCount.setdefault(word,0)
			wordCount[word]+=1
	return url, wordCount
def getWords(html):
	# Remove all the HTML tags
	txt = re.compile(r'<[^>]+>').sub('', html)
	# Split words by all non-alpha characters
	words = re.compile(r'[^A-Z^a-z]+').split(txt)
	# Convert to lowercase
	return [word.lower() for word in words if word != '']

apcount={}
wordcounts={}
feedlist= [line for line in file('feedlist.txt')]
for feedurl in feedlist:
	try:
		(url,wc) = getWordCount(feedurl)
		wordcounts[url]=wc
		for (word, count) in wc.items():
			apcount.setdefault(word,0)
			if count>1:
				apcount[word]+=1
	except:
		print 'failed to parse %s' % feedurl

wordlist=[]
for (word, blogcount) in apcount.items():
	frac= float(blogcount) / len(feedlist) # how many blogs used the word over total blogs
	if frac > 0.1 and frac < 0.5:
		wordlist.append(word)

out = file('blogdata1.txt', 'w')
out.write('Blog url')
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')
for (url, wc) in wordcounts.items():
    out.write(url.strip())
    for word in wordlist:
        if word in wc:
            out.write('\t%s' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')