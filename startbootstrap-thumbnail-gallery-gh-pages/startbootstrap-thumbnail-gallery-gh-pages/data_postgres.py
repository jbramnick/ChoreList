import psycopg2
import psycopg2.extras
from config import *

# Opens database connection for query execution
def connectToDB():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_HOST)
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
        return None
        
# Prototype for executing queries
def execute_query(query, conn, select=True, args=None):
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	results = None
	try: 
		quer = cur.mogrify(query, args) 
		print(quer)
		cur.execute(quer)
		if select:
			results = cur.fetchall()
		conn.commit()  
	except Exception as e:
		conn.rollback()
		print(type(e))
		print(e)
	cur.close()      
	return results

# Given a group_id, returns the id, name, stock, and cost of all rewards for the given group_id
def get_reward(group_id):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id, name, stock, cost as value FROM reward WHERE group_id = %s"
	results = execute_query(query_string, conn, args=(group_id, ))
	print(results)
	conn.close()
	return results
	
# Given a username, returns the group id and name of all groups the user is a user or admin of
def get_groups(username):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT g.id as id, g.name as name FROM groups g LEFT JOIN users u ON u.group_id = g.id left JOIN admin a ON a.group_id = g.id WHERE u.id = (SELECT id FROM usernames WHERE username = %s) OR a.id = (SELECT id FROM usernames WHERE username = %s);"
	results = execute_query(query_string, conn, args=(username, username))
	print(results)
	conn.close()
	return results
	
# Given a user, group_id, and points, updates that user in that group by adding points given to their current points total
def add_points(username, group_id, points):
	conn = connectToDB()
	if conn == None:
		return None
	query_string = "SELECT points FROM users WHERE id = (SELECT id FROM usernames WHERE username = %s) AND group_id = %s"
	testresults = execute_query(query_string, conn, args=(username, group_id))
	if testresults:
		total = int(testresults[0][0]) + points
		query_string1 = "UPDATE users SET points = %s WHERE id = (SELECT id FROM usernames WHERE username = %s AND group_id = %s)"
		execute_query(query_string1, conn, select=False,  args=(total, username, group_id))
		conn.close()
		return True
	conn.close()
	return False
	
# Given username, password, and newusername, changes the user's username if they have the currect user+pass info
def change_username(username, password, newusername):
	conn = connectToDB()
	if conn == None:
		return None
	query_string = "SELECT usernames.username FROM usernames JOIN pass ON pass.id = usernames.id WHERE usernames.username = %s AND pass.password = crypt(%s, password)"
	testresults = execute_query(query_string, conn, args=(username, password))
	query_string = "SELECT username FROM usernames WHERE username = %s"
	testresults2 = execute_query(query_string, conn, args=(newusername, ))
	if testresults and not testresults2:
		query_string1 = "UPDATE usernames SET username = %s WHERE username = %s"
		execute_query(query_string1, conn, select=False,  args=(newusername, username))
		conn.close()
		return True
	else:
		conn.close()
		return False
		
# Given username, password, and newusername, changes the user's password if they have the currect user+pass info
def change_password(username, password, newpassword):
	conn = connectToDB()
	if conn == None:
		return None
	query_string = "SELECT usernames.username FROM usernames JOIN pass ON pass.id = usernames.id WHERE usernames.username = %s AND pass.password = crypt(%s, password)"
	testresults = execute_query(query_string, conn, args=(username, password))
	if testresults:
		query_string1 = "UPDATE pass SET password = crypt(%s, gen_salt('bf')) WHERE password = crypt(%s, password)"
		execute_query(query_string1, conn, select=False,  args=(newpassword, password))
		conn.close()
		return True
	else:
		conn.close()
		return False
	
# given username, group_id, and points, sets the user's points for the specified group to the points given
def edit_points(username, group_id, points):
	conn = connectToDB()
	if conn == None:
		return None
	query_string = "SELECT points FROM users WHERE id = (SELECT id FROM usernames WHERE username = %s) AND group_id = %s"
	testresults = execute_query(query_string, conn, args=(username, group_id))
	if testresults:
		query_string1 = "UPDATE users SET points = %s WHERE id = (SELECT id FROM usernames WHERE username = %s AND group_id = %s)"
		execute_query(query_string1, conn, select=False,  args=(points, username, group_id))
		conn.close()
		return True
	conn.close()
	return False

# Given group_id, returns the id, name, and points of all chores in that group
def get_all_chores(group_id):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id, name, rewardVal as points FROM chore WHERE group_id = %s"
	results = execute_query(query_string, conn, args=(group_id, ))
	print(results)
	conn.close()
	return results

# Given username, and password, returns true if the user and pass combination is valid, false otherwise
def get_user(username, password):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT p.id FROM pass p JOIN usernames u ON u.id = p.id WHERE u.username = %s AND p.password = crypt(%s,password)"
	results = execute_query(query_string, conn, args=(username, password))
	print(results)
	conn.close()
	if results:
		return True
	else:
		return False
	
# given username, returns the user's points and group_name of all groups the user is a part of in a list of dictionaries
def get_auth(username):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT u.points as points, g.name as group_name FROM users u JOIN groups g ON g.id = u.group_id WHERE u.id = (SELECT id FROM usernames WHERE username = %s)"
	results = execute_query(query_string, conn, args=(username, ))
	print(results)
	conn.close()
	return results

# given username, password, and name, checks if the user is already registers and returns false if they are, otherwise inserts the user into the usernames and pass tables
def register_user(username, password, name):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT username FROM usernames WHERE username = %s"
	results2 = execute_query(query_string, conn, args=(username,))
	results = None
	if not results2:
		query_string = "INSERT INTO usernames (username, name) VALUES(%s, %s)"
		results = execute_query(query_string, conn, select=False, args=(username, name))
		query_string = "INSERT INTO pass (id, password) VALUES((SELECT id FROM usernames WHERE username = %s), crypt(%s, gen_salt('bf')))"
		results = execute_query(query_string, conn, select=False, args=(username, password))
		conn.close()
		return True
	print("Stuff is done")
	conn.close()
	return False
	
# given group_name and username, checks if the group already exists for that user and returns false if it does, otherwise adds that group along with that user as an admin
def add_group(group_name, username):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id FROM groups WHERE name = %s AND admin_id = (SELECT id FROM usernames WHERE username = %s)"
	results2 = execute_query(query_string, conn, args=(group_name, username))
	results = None
	if not results2:
		query_string = "INSERT INTO groups (name, admin_id) VALUES(%s, (SELECT id FROM usernames WHERE username = %s))"
		results = execute_query(query_string, conn, select=False, args=(group_name, username))
		query_string = "INSERT INTO admin (id, group_id) VALUES((SELECT id FROM usernames WHERE username = %s), (SELECT id FROM groups WHERE admin_id = (SELECT id FROM usernames WHERE username = %s) AND name = %s))"
		results = execute_query(query_string, conn, select=False, args=(username, username, group_name))
		conn.close()
		return True
	print("Stuff is done")
	conn.close()
	return False
	
# given a group_name and username, checks if a user is already in the group and returns False if they are, otherwise inserts them into the group by adding them to the users table for that group
def add_to_group(group_name, username):
	conn=connectToDB()
	if conn == None:
		return None
		
	query_string = "SELECT id FROM users WHERE group_id = (SELECT id FROM groups WHERE name = %s) AND id = (SELECT id from usernames WHERE username = %s)"
	results = execute_query(query_string, conn, args=(group_name, username))
	if not results:
		query_string = "INSERT INTO users (id, group_id) VALUES((SELECT id FROM usernames WHERE username = %s), (SELECT id FROM groups WHERE name = %s))"
		results2 = execute_query(query_string, conn, select=False, args=(username, group_name))
		conn.close()
		return True
	conn.close()
	return False

# given the following information, adds a chore to the db for the given group_id
def add_chore(chore_name, description, point_val, claimed, group_id):
	conn=connectToDB()
	if conn == None:
		return None
		
	query_string = "INSERT INTO chore (name, description, rewardVal, claimed, group_id) VALUES(%s, %s, %s, %s, %s)"
	results2 = execute_query(query_string, conn, select=False, args=(chore_name, description, point_val, claimed, group_id))
	conn.close()
	return True
	
# given a chore_name and group_id, deletes chores cooresponding to that name in a certain group. Returns True if succeeded
def remove_chore(chore_name, group_id):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id FROM chore WHERE name = %s AND group_id = %s"
	results = execute_query(query_string, conn, args=(chore_name, group_id))
	if results:
		query_string = "DELETE FROM chore WHERE name = %s AND group_id = %s"
		results2 = execute_query(query_string, conn, select=False, args=(chore_name, group_id))
		conn.close()
		return True
	conn.close()
	return False
	
# given the following information, adds a reward to the specified group
def add_reward(reward_name, description, cost, stock, group_id):
	conn=connectToDB()
	if conn == None:
		return None
		
	query_string = "INSERT INTO reward (name, description, cost, stock, group_id) VALUES(%s, %s, %s, %s, %s)"
	results2 = execute_query(query_string, conn, select=False, args=(reward_name, description, cost, stock, group_id))
	conn.close()
	return True
	
# given a reward information (number = stock to remove), updates the stock for a reward to subtract number from stock. If this puts stock at 0, then it deletes the reward from the table. returns true if succeeded
def remove_reward(reward_name, group_id, number):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id FROM reward WHERE name = %s AND group_id = %s AND stock >= %s"
	results = execute_query(query_string, conn, args=(reward_name, group_id, number))
	if results:
		query_string = "UPDATE reward SET stock = (stock-%s) WHERE name = %s AND group_id = %s"
		results2 = execute_query(query_string, conn, select=False, args=(number, reward_name, group_id))
		query_string ="SELECT stock FROM reward WHERE name = %s AND group_id = %s"
		results3 = execute_query(query_string, conn, args=(reward_name, group_id))
		if results3[0]["stock"] == 0:
			query_string = "DELETE FROM reward WHERE name = %s AND group_id = %s"
			results2 = execute_query(query_string, conn, select=False, args=(reward_name, group_id))
		conn.close()
		return True
	conn.close()
	return False
	
# given a username, returns the id and name of all groups that user is an admin of
def get_admin_groups(username):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT g.id as id, g.name as name FROM groups g JOIN admin a ON a.group_id = g.id WHERE a.id = (SELECT id FROM usernames WHERE username = %s);"
	results = execute_query(query_string, conn, args=(username,))
	print(results)
	conn.close()
	return results