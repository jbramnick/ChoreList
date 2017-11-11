import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, session,redirect, flash 
from flask_bootstrap import Bootstrap
from config import *
import data_postgres as pg

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')
#call this method before every location except home and register
def auth():
	try:
		if not session['Username']:
			return False	
		else:
			return True
	except:
		return False
@app.route('/auth',methods=['POST'])
def authorization():
	if request.form['submit']=="Register":
		return redirect("/register")
	page=request.form["page"]
	try:
		results = pg.get_user(request.form['Username'], request.form['Password'])
		#LINE BELOW IS FOR UI DEVELOPMENT TESTING ONLY REMOVE THIS LINE FOR DEPLOYMENT
		if request.form['Username']:
			results=True
		if results:
			session['Username'] = request.form['Username']
			return redirect("/"+page)
		else:
			return redirect("/?failed=True&page="+page)
	except:
		return redirect("/?failed=True&page="+page)
@app.route('/registerLog',methods=['POST'])
def registerLog():
	#do database stuff here
	try: 
		#insert user into database
		session['Username']=request.form['Username']
		if(request.form['Password']==request.form['ConfirmPassword']):
			return redirect("/index")
		else:
			return redirect("/register?failed=True")
	except:
		return redirect("/register?failed=True")
@app.route('/')
def home():
	if not request.args:
		return render_template('login.html',page="chores",login=True)	
	return render_template('login.html',failed=request.args["failed"],page=request.args["page"],login=True)
@app.route('/register')
def register():
	if not request.args:
		return render_template('register.html',login=True)
	else:
		return render_template('register.html',failed=request.args["failed"],login=True)
@app.route('/about')
def about():
	if not auth():
		return redirect("/?page=about&failed=False")
	return render_template('about.html',username=session['Username'],aboutPage="active")
@app.route('/rewards')
def rewards():
	if not auth():
		return redirect("/?page=rewards&failed=False")
	return render_template('rewards.html',rewardsPage="active",username=session['Username'])
@app.route('/chores')
def index():
	if not auth():
		return redirect("/?page=chores&failed=False")
	thing=[[1,2,3],[4,5,6]]
	#should prolly put database stuff here
	try:
		if not request.args["choreLog"]:
			choreLog=None
		else:
			choreLog=request.args["choreLog"]
	except:
		choreLog=None
	print(choreLog)
	return render_template('chores.html',username=session['Username'],choresPage="active",things=thing,choreLog=choreLog)
@app.route('/profile')
def profile():
	if not auth():
		return redirect("/?page=profile&failed=False")
	return render_template('profile.html',username=session['Username'],profilePage="active")
@app.route('/choreLog')
def choreLog():
	#remove chore from database
	return redirect("/chores?choreLog=True")
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
