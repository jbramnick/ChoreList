import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, session,redirect, flash 
from flask_bootstrap import Bootstrap
from config import *
import data_postgres as pg

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

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
				points=userinfo[0][1]
				session['Points'] = points
				session['Group'] = None
				session['Groups']=pg.get_groups(request.form['Username'])
				return redirect("/"+page+"?GroupId="+session['Group'])
			else:  
				session['Username']=request.form['Username']
				session['Points']=None
				session['Group']=None
				session['Groups']=pg.get_groups(request.form['Username'])
				print(session['Groups'])

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
		session['Groups']=None
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
	
	return redirect("/chores?choreLog=True")
	
@app.route('/rewardLog')
def rewardLog():
	
	return redirect("/rewards?rewardLog=True")
	
@app.route('/profileDelta',methods=['POST'])
def profileDelta():
	if not auth():
		return redirect("/?page=profile&failed=False")
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
	print(newUsername)
	if(newUsername):
		if not pg.change_username(session['Username'],oldPassword,newUsername):
			return redirect("/profile?FailedUsername=True")
		session['Username']=newUsername
	if(oldPassword and newPassword and confirmNew):
		if(newPassword==confirmNew):
			if not pg.change_password(session['Username'],oldPassword,newPassword):
				return redirect("/profile?FailedOld=True")
		else:
			return redirect("/profile?FailedConfirm=True")
	return redirect("/profile")
@app.route('/groupChange')
def groupChange():
	session['Group']=request.args['group']
	return redirect("/chores")
@app.route('/createGroupLog',methods=['POST'])
def createGroupLog():
	if not auth:
		return redirect("/?page=createGroup&failed=False")
	pg.add_group(request.form['Groupname'],session['Username'])
	session['Groups']=session['Groups']+[[None,str(request.form['Groupname'])]]
	return redirect("/createGroup")
@app.route('/logOut')
def logOut():
	session.clear()
	return redirect("/")
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
	points=session['Points'],\
	groups=session['Groups'],\
	group=session['Group'])
@app.route('/help')
def help():
	if not auth():
		return redirect("/?page=help&failed=False")
	return render_template('Help.html',\
	username=session['Username'],\
	helpPage="active",\
	points=session['Points'],\
	groups=session['Groups'],\
	group=session['Group'])

@app.route('/createGroup')
def createGroup():
	if not auth():
		return redirect("/?page=createGroup&failed=False")
	return render_template('createGroup.html',\
	username=session['Username'],\
	createGroupPage="active",\
	points=session['Points'],\
	groups=session['Groups'],\
	group=session['Group'])
@app.route('/rewards')
def rewards():
	if not auth():
		return redirect("/?page=rewards&failed=False")
	
	thing2 = pg.get_reward(session['Group'])
	
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
	groups=session['Groups'],\
	group=session['Group'])
	
@app.route('/chores')
def index():
	if not auth():
		return redirect("/?page=chores&failed=False")
	thing=[[1,2,3],[4,5,6]]
	
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
	group=session['Group'],\
	groups=session['Groups'])
@app.route('/profile')
def profile():
	if not auth():
		return redirect("/?page=profile&failed=False")
	try:
		failedConfirm=request.args["FailedConfirm"]
	except:
		failedConfirm=None
	try:
		failedUsername=request.args["FailedUsername"]
	except:
		failedUsername=None
	if(failedConfirm):
		return render_template('profile.html',\
		username=session['Username'],\
		profilePage="active",\
		points=session['Points'],\
		group=session['Group'],\
		groups=session['Groups'],\
		failedConfirm=failedConfirm)
	if(failedUsername):
		return render_template('profile.html',\
		username=session['Username'],\
		profilePage="active",\
		points=session['Points'],\
		group=session['Group'],\
		groups=session['Groups'],\
		FailedUsername=failedUsername)
	return render_template('profile.html',\
	username=session['Username'],\
	profilePage="active",\
	points=session['Points'],\
	groups=session['Groups'],\
	group=session['Group'])
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
