import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, session,redirect 
from flask_bootstrap import Bootstrap
from config import *
import data_postgres as pg

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')
@app.route('/auth',methods=['POST'])
def authorization():
	if request.form['submit']=='Login':
		try:
			results = pg.get_user(request.form['Username'], request.form['Password'])
			#LINE BELOW IS FOR UI DEVELOPMENT TESTING ONLY REMOVE THIS LINE FOR DEPLOYMENT
			results=True
			if results:
				session['Username'] = request.form['Username']
				session['Password'] = request.form['Password']
				return redirect("/index")
			else:
				return redirect("/?failed=True")
		except:
			return redirect("/?failed=True")
	elif request.form['submit']=='Register':
		return redirect("/register")
def auth():
	try:
		if not session['Username']:
			return False	
		else:
			return True
	except:
		return False
@app.route('/')
def home():
	if not request.args:
		return render_template('login.html', login=True)	
	elif request.args["failed"]:
		return render_template('login.html',failed=request.args["failed"],login=True)
@app.route('/register')
def register():
	return render_template('login.html',disabled="disabled",login=True)
@app.route('/about')
def about():
	if not auth():
		return redirect("/")
	return render_template('about.html',username=session['Username'],aboutPage="active")
@app.route('/rewards')
def rewards():
	if not auth():
		return redirect("/")
	return render_template('rewards.html',rewardsPage="active",username=session['Username'])
@app.route('/index')
def index():
	if not auth():
		return redirect("/")
	thing=[1,2,3,4,5,6,7]
	#should prolly put database stuff here
	return render_template('index.html',username=session['Username'],chorePage="active",things=thing)
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
