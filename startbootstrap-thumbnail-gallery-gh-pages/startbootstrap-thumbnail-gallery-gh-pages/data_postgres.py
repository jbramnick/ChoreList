import psycopg2
import psycopg2.extras
from config import *

def connectToDB():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_HOST)
    try:
        return psycopg2.connect(connectionString)
    except:
        #print("Can't connect to database")
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


def get_champion():
    conn = connectToDB()
    if conn == None:
        return None
    query_string = "SELECT name FROM champions"
    results = execute_query(query_string, conn)
    #print(results)
    conn.close()
    return results
    
def get_items():
    conn = connectToDB()
    if conn == None:
        return None
    query_string = "SELECT name FROM items"
    results = execute_query(query_string, conn)
    #print(results)
    conn.close()
    return results
    
def get_summoners():
    conn = connectToDB()
    if conn == None:
        return None
    query_string = "SELECT name FROM summoners"
    results = execute_query(query_string, conn)
    #print(results)
    conn.close()
    return results
    
def get_keystones():
    conn = connectToDB()
    if conn == None:
        return None
    query_string = "SELECT name FROM keystone"
    results = execute_query(query_string, conn)
    #print(results)
    conn.close()
    return results
    
def get_boots():
    conn = connectToDB()
    if conn == None:
        return None
    query_string = "SELECT name FROM boots"
    results = execute_query(query_string, conn)
    #print(results)
    conn.close()
    return results