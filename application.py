import os

from flask import Flask, render_template, request, session, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""
#localhost connection settings
app.config['MYSQL_USER']='flask'
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='flights'
app.config['MYSQL_CURSORCLASS']='DictCursor'
"""
#aws connection settings
app.config['MYSQL_USER']='admin'
app.config['MYSQL_PASSWORD']="Amazonjuli10"
app.config['MYSQL_HOST']='mydbinstance.cpdtaxzar9ga.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DB']='dav6100_db'
app.config['MYSQL_CURSORCLASS']='DictCursor'

#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

mysql=MySQL(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/profile', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    cur = mysql.connection.cursor()
    #if request.form['password'] == 'password' and request.form['username'] == 'admin':
    #https://pynative.com/python-mysql-select-query-to-fetch-data/
    select_query="""SELECT * FROM users WHERE username = %s and password = %s"""
    select_parms = (POST_USERNAME, POST_PASSWORD)
    cur.execute(select_query, select_parms)
    
    users = cur.fetchall()

    if cur.rowcount == 1:
        session['logged_in'] = True
    else:
        return('wrong password!')
    

    return render_template("profile.html", users=users)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/register_new", methods=["POST"])
def register_new():

    cur = mysql.connection.cursor()
    #if request.form['password'] == 'password' and request.form['username'] == 'admin':
    #https://pynative.com/python-mysql-select-query-to-fetch-data/
    select_query="""SELECT * FROM health_condition"""
    cur.execute(select_query)
    
    health_conditions = cur.fetchall()

    return render_template("register.html", conditions=health_conditions)

@app.route('/register_submit', methods=['POST'])
def register_submit():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    POST_EMAIL = str(request.form['email'])
    POST_HEALTH_CONDITIONS = request.form['healthCondition']

    cur = mysql.connection.cursor()

    insert_query="""INSERT INTO users (username, password, email) value (%s, %s, %s)"""
    insert_parms = (POST_USERNAME, POST_PASSWORD, POST_EMAIL)
    cur.execute(insert_query, insert_parms)

    mysql.connection.commit()
    return render_template("profile.html")

@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    return ""


@app.route("/main")
def main():
    cur = mysql.connection.cursor()
    cur.execute("Select * from r_ctry LIMIT 5")
    flights=cur.fetchall()
    #return "Done"
    #flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)