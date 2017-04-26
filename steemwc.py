import dateutil.parser
import re
import sys
import matplotlib.pyplot as plt
import numpy as np
import pymongo

from os import path
from PIL import Image
from pymongo import MongoClient
from steemdata import SteemData
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = sys.argv[1]
dtest = re.compile("^\d{4}-(0\d|1[0-2])-([0-2]\d|3[01])$")

try:
	dtest.match(d)
except: 
	print("Date must be in the format YYYY-MM-DD: ", d)
	sys.exit(1)

# Start and end times of the date passed into the program
start = dateutil.parser.parse(d + "T00:00:00.000Z")
end = dateutil.parser.parse(d + "T23:59:59.000Z")

# Hookup with the steemdata MongoDB service
s = SteemData()

# Get the top 100 posts by vote for DATE
posts = s.Posts.find({"created":{'$gte':start,'$lt':end}}).sort("net_votes", pymongo.DESCENDING).limit(100)

# word cloud text
text = ""

for p in posts:
	from bs4 import BeautifulSoup
	
	# Get HTML-stripped text of post body
	b = BeautifulSoup(p['body'], 'html.parser').get_text()

	# Strip out markdown image/URL code
	b = re.sub(r'!?\[.*?\]\(http.*?\)', r'', b)
	
	# Strip other URLs
	b = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', b)
			
	# append cleaned body of current record to the word cloud text
	text += b

# Set directory path
dir = path.dirname(__file__)

# Open steemit logo mask image
mask = np.array(Image.open(path.join(dir, "steemit-logo-mask.png")))

# Set stopwords, add custom stopwords
stopwords = set(STOPWORDS)
sw = open("stopwords.txt").read().splitlines()
for w in sw:
	stopwords.add(w)

# Create word cloud data
wc = WordCloud(font_path="/users/curtis/Library/Fonts/ProximaNovaSoft-Semibold.otf", background_color="white", max_words=2000, mask=mask,
               stopwords=stopwords)

# Generate word cloud image
wc.generate(text.lower())

# Save image to PNG file
imgfile = "steemitwc-" + d + ".png"
wc.to_file(path.join(dir, imgfile))