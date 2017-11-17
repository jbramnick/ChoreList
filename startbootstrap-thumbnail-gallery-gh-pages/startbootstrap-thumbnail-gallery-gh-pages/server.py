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
		if results:
			userinfo = pg.get_auth(request.form['Username'])
			print(userinfo)
			session['Username'] = request.form['Username']
			if userinfo:
				session['Name'] = userinfo[0][0]
				points=userinfo[0][1]
				session['Points'] = points
				session['Group'] = userinfo[0][2]
				return redirect("/"+page+"?GroupId="+session['Group'])
			else:  
				session['Username']=request.form['Username']
				session['Points']=0
				session['Group']=None
				return redirect("/"+page)
		else:
			return redirect("/?failed=True&page="+page)
	except:
		return redirect("/?failed=True&page="+page)
		
@app.route('/registerLog',methods=['POST'])
def registerLog():
	try: 
		session['Username']=request.form['Username']
		session['Group']=None
		session['Points']=0
		if(request.form['Password']==request.form['ConfirmPassword']):
			registerSuccess = pg.register_user(request.form['Username'],request.form['Password'],\
			request.form['Fullname'])
			if(registerSuccess):
				return redirect("/chores")
			else:
				return redirect("/register?failed=True")
		else:
			return redirect("/register?failed=True")
	except:
		return redirect("/register?failed=True")
		
@app.route('/choreLog')
def choreLog():
	#DATABASE
	#remove chore from database
	#MB# Do you want to remove a specific chore? if so give me the variable I need to identify which chore
	#im going to pass you a chore id to remove rather to set to awaiting verification or whatever it will likely be
	#request.args['choreId']
	return redirect("/chores?choreLog=True")
	
@app.route('/rewardLog')
def rewardLog():
	#DATABASE
	#MB# please provide name of the request.form[''] variable to identify the reward
	#its going to be a request.args['rewardId'] not form since im passing it through a link not a form submit
	#remove a rewards stock from database
	#also change the session['Points'] value 
	#Change it for the user
	return redirect("/rewards?rewardLog=True")
	
@app.route('/profileDelta',methods=['POST'])
def profileDelta():
	try:
		oldPassword=request.form['OldPassword']
	except:
		oldPassword=None
	try:
		newPassword=request.form['NewPassword']
	except:
		newPassword=None
	try:
		confirmNew=request.form['ConfirmNewPassword']
	except:
		confirmNew=None
	try:
		newUsername=request.form['Username']
	except:
		newUsername=None
	if(oldPassword and newPassword and confirmNew):
		if(newPassword==confirmNew):
			if not pg.change_password(session['Username'],oldPassword,newPassword):
				return redirect("/profile?FailedOld=True")
		else:
			return redirect("/profile?FailedConfirm=True")
	if(newUsername):
		if not pg.change_username(session['Username'],oldPassword,newUsername):
			session['Username']=newUsername
			return redirect("/profile?FailedUsername=True")
	return redirect("/profile")
	
@app.route('/')
def home():
	if not request.args:
		return render_template('login.html',page="chores",login=True)	
	return render_template('login.html',failed=request.args["failed"],page=request.args["page"],login=True)
	
@app.route('/register')
def register():
	#MB# Below is the function to register a new user, it already checks if the user exists. It will return true if it succeeds and false if the username already exists
	

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
	points=session['Points'],\
	group=session['Group'])
@app.route('/rewards')
def rewards():
	if not auth():
		return redirect("/?page=rewards&failed=False")
	#DATABASE
	#MB# Specify what database values for what you need here. Is it just a list of rewards? if so what values do you need?
	#ANSWER-Need another list of lists here with the same group session variable(session['group']) 
	#format of list
	
	#[reward id, reward name, reward stock, reward point value]
	thing2 = pg.get_reward(session['Group'])
	# Above lists all rewards for a group in the format [id, name, stock, value]
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
	#DATABASE
	points=session['Points'],\
	group=session['Group'])
	
@app.route('/chores')
def index():
	if not auth():
		return redirect("/?page=chores&failed=False")
	thing=[[1,2,3],[4,5,6]]
	#ANSWER-Need a list of lists the list being all chores for the group that the user is in
	#i will pass you a group variable likely going to be session['Group']
	#the format of the list should be this
	#chores = pg.get_all_chores(session['Group'])
	#MB# The above gets all chores whether claimed or not in the structure [id, name, points] 
	#[chore id,chore name,chore point value]
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
	points=session['Points'],\
	group=session['Group'])
@app.route('/profile')
def profile():
	if not auth():
		return redirect("/?page=profile&failed=False")
	try:
		failedConfirm=request.args["FailedConfirm"]
	except:
		failedConfirm=None
	if(failedConfirm):
		return render_template('profile.html',\
		username=session['Username'],\
		profilePage="active",\
		points=session['Points'],\
		group=session['Group'],\
		failedConfirm=failedConfirm)
	return render_template('profile.html',\
	username=session['Username'],\
	profilePage="active",\
	points=session['Points'],\
	group=session['Group'])
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
