import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, session,redirect 
from flask_bootstrap import Bootstrap
from config import *
import data_postgres as pg

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

@app.route('/')
def home():
	if request.args["failed"]:
		return render_template('login.html',failed=request.args["failed"])
	return render_template('login.html')
@app.route('/register')
def register():
	return render_template('login.html',disabled="disabled")
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/index',methods=['POST'])
def index():
	if request.form['submit']=='Login':
		try:
			results = pg.get_user(request.form['Username'], request.form['Password'])
			if results:
				session['Username'] = request.form['Username']
				session['Password'] = request.form['Password']
				#session['id'] = results[0][2]
				thing=[1,2,3,4,5,6,7]
				#put database queries here
				return render_template('index.html',things=thing,username=user)
			else:
				return redirect("/?failed=True")
		except:
			return render_template("login.html", failed=True)
	elif request.form['submit']=='Register':
		return redirect("/register")
		
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
