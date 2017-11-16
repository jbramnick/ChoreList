import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, session,redirect, flash 
from flask_bootstrap import Bootstrap
from config import *
import data_postgres as pg

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')
#call this method before every user page
def auth():
	try:
		if not session:
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
		#LINES BELOW ARE FOR UI DEVELOPMENT TESTING ONLY REMOVE THESE LINES FOR DEPLOYMENT
		if request.form['Username']:
			results=True
		#END UI TESTING LINES
		if results:
			userinfo = pg.get_auth(request.form['Username'])
			#MB# The above returns a list of lists with these elements: [name, points, group_name]
			#MB# This is to join a default group (the first group in the list)
			session['Username'] = request.form['Username']
			if userinfo:
				points=userinfo[0][1]
				session['Points'] = points
				#MB# Added session Group for the name of the group the user defaults to on login
				session['Group'] = userinfo[0][2]
			else: #MB# Added if/else. If userinfo does not have any rows it is because the user is not a part of any groups yet.
				#MB# Please add here whatever you need to render a page with no groups yet. Make sure front end handles no group session and no points session variables
				session['Points'] = 0
			return redirect("/"+page)
		else:
			return redirect("/?failed=True&page="+page)
	except:
		return redirect("/?failed=True&page="+page)
		
@app.route('/registerLog',methods=['POST'])
def registerLog():
	#DATABASE
	#MB# Can you confirm what you want here and what registerLog does? 
	try: 
		#insert user into database
		#DATABASE
		session['Username']=request.form['Username']
		session['Points']=20
		if(request.form['Password']==request.form['ConfirmPassword']):
			#MB# do you want adding to the database to be done here, only when passwords match?
			return redirect("/index")
		else:
			return redirect("/register?failed=True")
	except:
		return redirect("/register?failed=True")
		
@app.route('/choreLog')
def choreLog():
	#DATABASE
	#remove chore from database
	#MB# Do you want to remove a specific chore? if so give me the variable I need to identify which chore
	return redirect("/chores?choreLog=True")
	
@app.route('/rewardLog')
def rewardLog():
	#DATABASE
	#MB# please provide name of the request.form[''] variable to identify the reward
	#remove a rewards stock from database
	#also change the session['Points'] value 
	#Change it for the user
	return redirect("/rewards?rewardLog=True")
	
@app.route('/profileDelta',methods=['POST'])
def profileDelta():
	#DATABASE
	#MB# Please list the info you need for the profile
	return redirect("/profile")
	
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
	return render_template('About.html',\
	username=session['Username'],\
	aboutPage="active",\
	points=session['Points'])
@app.route('/rewards')
def rewards():
	if not auth():
		return redirect("/?page=rewards&failed=False")
	#DATABASE
	#MB# Specify what database values for what you need here. Is it just a list of rewards? if so what values do you need?
	thing=[[1,2,3],[4,5,6]]
	try:
		if not request.args["rewardLog"]:
			rewardLog=None
		else:
			rewardLog=request.args["rewardLog"]
	except:
		rewardLog=None
	return render_template('rewards.html',\
	rewardsPage="active",\
	username=session['Username'],\
	things=thing,\
	rewardLog=rewardLog,\
	points=session['Points'])
	
@app.route('/chores')
def index():
	if not auth():
		return redirect("/?page=chores&failed=False")
	thing=[[1,2,3],[4,5,6]]
	#DATABASE
	#MB# Specify what database values for what you need here. Is it just a list of Chores? if so what values do you need?
	try:
		if not request.args["choreLog"]:
			choreLog=None
		else:
			choreLog=request.args["choreLog"]
	except:
		choreLog=None
	return render_template('chores.html',\
	username=session['Username'],\
	choresPage="active",\
	things=thing,\
	choreLog=choreLog,\
	points=session['Points'])
	
@app.route('/profile')
def profile():
	#DATABASE
	#MB# please specify what data you need
	if not auth():
		return redirect("/?page=profile&failed=False")
	return render_template('profile.html',\
	username=session['Username'],\
	profilePage="active",\
	points=session['Points'])
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
