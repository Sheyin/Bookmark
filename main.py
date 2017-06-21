from flask_pymongo import PyMongo
from flask import Flask, Response, render_template, request
import secret
import datetime
import pprint	# Make objects look nicer in console
from pymongo import MongoClient
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
		# ex. searchword = request.args.get('key', '') - 
		# retrieves url parameters(?key=value)
	elif request.method == 'POST':
		# might be request.form.name
		name = request.form['name']
		url = request.form['url']
		description = request.form['description']
		tags = request.form['tags']
		addedBy = request.form['addedBy']
		print ("Name: " + name + " url: " + url)
		print ("Description: " + description + " Tags: " + str(tags))
		print ("Added by: " + addedBy)
		# Send data to db
		# Return some response
		return render_template('added.html', name=name)

@app.route("/get")
def retrieveSite():
	searchword = request.args.get('key', '')
	site = db.find_one({"name": searchword})
	#site = mongo.db.collectionname.find_one_or_404({'name': searchword})
	#pprint.pprint("site: " + str(site))
	if not site:
		return render_template('notfound.html', searchword=searchword)
	else:
		return render_template('found.html', name=site['name'], url=site['url'], dateVisited=site['dateVisited'])

@app.route("/")
def showHub():
	return render_template('hub.html')

if __name__ == "__main__":
    app.run()