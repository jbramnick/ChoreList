import psycopg2
import psycopg2.extras
from config import *

def connectToDB():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_HOST)
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
        return None
        
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

def get_reward(group_id):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id, name, stock, cost as value FROM reward WHERE group_id = %s"
	results = execute_query(query_string, conn, args=(group_id, ))
	print(results)
	conn.close()
	return results

def get_all_chores(group_id):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id, name, rewardVal as points FROM chore WHERE group_id = %s"
	results = execute_query(query_string, conn, args=(group_id, ))
	print(results)
	conn.close()
	return results

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
	
def get_auth(username):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT u.name as name, u.points as points, g.name as group_name FROM users u JOIN groups g ON g.id = u.group_id WHERE u.id = (SELECT id FROM usernames WHERE username = %s)"
	results = execute_query(query_string, conn, args=(username, ))
	print(results)
	conn.close()
	return results

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
    
def new_player(username, password, name):
	conn = connectToDB()
	if conn == None:
		return None
	query_string = "SELECT id FROM usernames WHERE username = %s"
	testresults = execute_query(query_string, conn, args=(username,))
	if not testresults:
	    query_string1 = "INSERT INTO usernames (username, name) VALUES (%s, %s)"
	    execute_query(query_string1, conn, select=False,  args=(username,name))
	
	    query_string2 = "INSERT INTO pass (id, password) VALUES ((SELECT id FROM usernames WHERE username = %s), crypt(%s, gen_salt('bf')))"
	    execute_query(query_string2, conn, select=False,  args=(username, password))
	    conn.close()
	    return 1
	conn.close()
	return 0