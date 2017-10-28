# #need at least all this to do form request
# import psycopg2
# import psycopg2.extras
import os
from flask import Flask, render_template
app = Flask(__name__)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def mainIndex():
    

    return render_template('HomePage.html') # you had TemplateBase.html



#start the server (very basic)
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)

 #more advanced
if __name__ == '__main__':
     app.debug=True
     app.run(host='0.0.0.0', port=8080)