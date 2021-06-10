from flask import Flask,render_template,g,request,flash,redirect,url_for,session,flash
from functools import wraps
import sqlite3
import os
import random
from flask.templating import render_template_string

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

app.secret_key = os.urandom(24)
app.database='user_db.sqlite'
conn=sqlite3.connect('user_db.sqlite')


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/search')
def sef():
    return render_template('search.html')


@app.route('/', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        global uname
        username = request.form['username']
        password = request.form['password']
        if request.form.get("sign_up"):
            try:
                if username and password:
                    conn = sqlite3.connect(app.database)
                    cur = conn.cursor()
                    cur.execute("INSERT INTO users(username,password) VALUES (?,?)", (username,password))
                    conn.commit()
                    conn.close()
                    flash('Registration succesfull!')
            except sqlite3.Error as e:
                flash("User has already been created. ")
        elif request.form.get("login"):
            conn = sqlite3.connect(app.database)
            cur = conn.cursor()
            cur.execute("SELECT username, password FROM users WHERE username == ? and password == ?", (username, password))
            user = cur.fetchone()
            if not user:
                error = 'Invalid Credentials. Please try again.'
            else:
                uname = username
                session['logged_in']=True 
                return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route('/definition')
def rec(): 
    g.db = connect_db('words.sqlite') 
    cur = g.db.execute('SELECT word, word_definition FROM word_list')

    row = cur.fetchall()  
    return render_template('index.html',row=row)
@app.route('/rec1')


@app.route('/search',methods=['POST'])
def ser():

    g.db = connect_db('words.sqlite')
    cur=g.db.execute( "SELECT word, word_definition FROM word_list WHERE word = ? ", (request.form['search'].lower(),) )
    row = cur.fetchall()
    if not row:
        flash('word not found!')
        return render_template("search.html",row=row)
    else:
        return render_template("index.html",row=row)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    flash('!!You were just logged out')
    return redirect(url_for('login'))


@app.route('/practice',methods=['POST'])
@login_required
def practice():
    g.db = connect_db('word_practice.sqlite')
    cur = g.db.execute("SELECT * FROM practice WHERE username == ?;", (uname,))
    row = cur.fetchall()
    if len(row) < 10:
        flash('In order to practice, you must add at least 10 words to your dictionary!')
        return render_template("pract.html")
    else:
        pass
        g.db = connect_db()
        g.db.execute( "SELECT")
        g.db.commit()
        cur=g.db.execute( "SELECT")
        row=cur.fetchall()
        return render_template("practice.html",row=row) 


@app.route('/pract')
@login_required
def pract():
    return render_template('pract.html')


@app.route('/search')
def search():
    return render_template("search.html")
def connect_db(db=app.database):
    return sqlite3.connect(db)




if __name__ == '__main__':
    app.run(debug=True)
