import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from config import *
#import data_postgres as pg

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'Som3thing';

@app.route('/')
def home():
    thing = ['1', '2', '3', '4', '5']
    return render_template('index.html', things = thing)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
