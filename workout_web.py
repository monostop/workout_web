# all the imports
from __future__ import with_statement
from contextlib import closing
import sqlite3
import dateutil.parser
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash, make_response
from plotvalues import plot_total, plot_month
import gc

# TOOO ERROR HANDELING IN ADD!
#create app
app = Flask(__name__)
app.config.from_object('config')

# functions for init and connecting the db
def connect_db():    
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def main_page():
    return render_template('login.html')

@app.route('/add', methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        try:                
            if bool(request.form['date']) and dateutil.parser.parse(request.form['date']):
                # if user submits empty string dont insert anything into db.        
                dateutil.parser.parse(request.form['date'])                  
                g.db.execute('INSERT INTO '+session['user']+ '(date,value) VALUES (?,?)', \
                                 [request.form['date'],request.form['value']] ) 
                g.db.commit() 
                flash('Workout successfully submitted')   
            else:
                flash('No workout submitted, check formating!')         
        except ValueError:
            # need to print some error message.
            flash('No workout submitted, check formating!')
            pass              
    return render_template('add.html') 


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        if login not in app.config['USERNAMES']:
            error = 'Wrong login'
        elif login in app.config['USERNAMES'] and app.config['PASSWORD'].get(login) == request.form['password']:
            session['user'] = request.form['login']    
            session['logged_in'] = True
            flash('You are now logged in!') 
            return redirect(url_for('show_graph'))
        else:
            error = 'Wrong password'
    return render_template('login.html', error = error)
    

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main_page'))


@app.route('/progress', methods=['GET','POST'])
def show_graph():
    if request.method == 'POST':       
        session['month'] = request.form['month']   
    else:
        # Default to current month
        today = datetime.datetime.now()
        month = today.strftime("%m")
        session['month'] = month         
    return render_template('show_graph.html', month = session['month'])

    
@app.route('/graph.png')
def graph_url(): 
    values = {}
    dates = {}
    competitors = ['Viktor', 'Kim', 'Olof'] 
    for competitor in competitors:            
        sql = "SELECT * FROM "+competitor 
        cur = g.db.execute(sql)                          
        data = cur.fetchall() 
        dates_txt = [s[1] for s in data]
        values[competitor] = [i[2] for i in data]
        dates[competitor] = [dateutil.parser.parse(s) for s in dates_txt]
    
    month = int(session['month'])
    if month > 8:
        year = 2011
    else:
        year = 2012            
    
    if month == 0: # User clicked show all progress
        response = make_response(plot_total(competitors, dates, values)) 
    else:        
        response = make_response(plot_month(competitors, year, month, dates,
                                            values))
    gc.collect()
    response.headers['Conent-Type'] = 'image/png'
    return response
        
if __name__=="__main__":
    app.run()
