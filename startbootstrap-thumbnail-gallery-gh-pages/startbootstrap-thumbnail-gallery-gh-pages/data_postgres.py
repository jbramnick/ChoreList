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
		#print(quer)
		cur.execute(quer)
		if select:
			results = cur.fetchall()
		conn.commit()  
	except Exception as e:
		conn.rollback()
		#print(type(e))
		#print(e)
	cur.close()      
	return results


def get_user(username, password):
	conn=connectToDB()
	if conn == None:
		return None
	query_string = "SELECT p.id FROM pass p JOIN usernames u ON u.id = p.id WHERE u.username = %s AND p.password = crypt(%s,password)"
	results = execute_query(query_string, conn, args=(username, password))
	print(results)
	conn.close()
	return results
    
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