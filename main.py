from flask import Flask
from flask import render_template
import enginetest

app = Flask(__name__)

@app.route("/")
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route("/dead-in-the-water/")
def deadInTheWater():
	# What the console says
	console = enginetest.bottomLevelTest()
	return render_template('main.html', input=input)

@app.route("/dead-in-the-water/<input>")
def deadInTheWaterInput(input=None):
	return render_template('main.html', input=input)

if __name__ == "__main__":
    app.run()