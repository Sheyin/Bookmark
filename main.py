from flask_pymongo import PyMongo
from flask import Flask, Response, render_template, request
import secret
import datetime
import pprint	# Make objects look nicer in console
from pymongo import MongoClient
import re

db = secret.dbpath

app = Flask(__name__)
# Configuration for mongo / pymongo
app.config['MONGO_HOST'] = secret.host
app.config['MONGO_PORT'] = secret.port
app.config['MONGO_DBNAME'] = secret.dbname
mongo = PyMongo(app)

# Displays the form for adding a bookmark
@app.route("/create.html", methods=['GET', 'POST'])
@app.route("/create", methods=['GET', 'POST'])
@app.route("/new", methods=['GET', 'POST'])
def createBookmark():
	if request.method == 'GET':
		return render_template('create.html')
		# ex. searchword = request.args.get('key', '') 
		# retrieves url parameters(?key=value)
	elif request.method == 'POST':
		# might be request.form.name
		name = request.form['name']
		url = request.form['url']
		description = request.form['description']
		tags_whole = request.form['tags']
		tags_split = tags_whole.split(',')
		tags = []
		print ("tags: --" + str(tags) + "--")
		for item in tags_split:
			tags.append(item.rstrip())
		addedBy = request.form['addedBy']

		# Check if site already exists
		# This needs to be refined to check subdomain, allow subreddits etc
		regex = re.compile('\w*' + url + '\w*', re.IGNORECASE)
		site = ""
		# complete working query:
		site = db.find({"url": {"$regex": regex}})
		if site.count() > 0:
			return render_template('error.html', error="Site already exists.")
		else:
			# Send data to db
			result = db.insert_one({'name': name, 'url': url, 'description': description, 'tags': tags, 'dateVisited': datetime.datetime.now(), "lastVisited": datetime.datetime.now(), "snapshot": "null", "addedBy": addedBy})
			# Return some response
			if result.acknowledged:
				return render_template('added.html', name=name)
			else:
				return render_template('error.html', error="Unable to add bookmark.")

@app.route("/get")
@app.route("/search")
def retrieveSite():
	# Might need to limit combinations until a better way to pass arguments is learned
	searchTerm = request.args.get('name', '')
	searchTag = request.args.get('tag', '')
	
	if searchTerm:
		regex = re.compile('\w*' + searchTerm + '\w*', re.IGNORECASE)
		site = ""
		# complete working query:
		site = db.find({"name": {"$regex": regex}})
		#site = db.find({"$text": {"$search": searchTerm }})
		# debug - Error: text index required for $text query
		name = ""
		url = ""
		desciption = ""
		dateVisited = ""
		results = []
		for doc in site:
			name = doc['name']
			url = doc['url']
			description = doc['description']
			dateVisited = doc['dateVisited']
			results.append((name, url, description, dateVisited))
			pprint.pprint(doc)
		if site.count() > 0:
			return render_template('found.html', results=results)
		else:
			return render_template('found.html', searchword=searchTerm)
	
	# search by category
	elif searchTag:
		#regex = re.compile('\w*' + searchTag + '\w*', re.IGNORECASE)
		site = ""
		site = db.find({"tags": searchTag})
		#site = db.find({"tags": {"$regex": regex}})
		name = ""
		url = ""
		desciption = ""
		dateVisited = ""
		results = []
		for doc in site:
			name = doc['name']
			url = doc['url']
			description = doc['description']
			dateVisited = doc['dateVisited']
			results.append((name, url, description, dateVisited))
			pprint.pprint(doc)
		if site.count() > 0:
			return render_template('foundTag.html', results=results, tag=searchTag)
		else:
			return render_template('foundTag.html', tag=searchTag)
	# No arguments, just getting to search page 
	else:
		# Get all the possible tags from the database
		site = db.find().distinct("tags")
		categories = []
		for doc in site:
			pprint.pprint(doc)
			categories.append(doc)
		return render_template('search.html', categories=categories)
		


@app.route("/")
def showHub():
	return render_template('hub.html')


# This is the experimental code to get multiple field searches
def searchMultiple():
	# List of variables to get from request url
	'''
	searchName = ("name", request.args.get("name"))
	searchUrl = ("url", request.args.get("url"))
	searchTag = ("tags", request.args.get("tag"))
	searchDescription = ("description", request.args.get("description"))
	searchDateRange = ("dateVisited", request.args.get("dateRange"))
	#regex2 = re.compile('\w*' + 'programming' + '\w*')
	#site = db.find({"name": {"$regex": regex}, "tags": {"$regex": regex2}})

	regphrase = '": {$regex: '
	searchList = [searchName, searchUrl, searchTag, searchDescription, searchDateRange]
	query = "{"
	reglist = []
	querylist = []
	separator = '}, '

	for searchTerm in searchList:
		print (searchTerm)
		if searchTerm[1] != None:
			print (searchTerm[1])
			reglist.append(re.compile('\w*' + searchTerm[1] + '\w*'))
			#regex = re.compile('\w*' + searchTerm[1] + '\w*')
			query += '\"' + searchTerm[0] + regphrase
	# end query string with bracket
	query += "}"
	'''
	return


if __name__ == "__main__":
    app.run()