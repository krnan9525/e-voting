# all the imports
from flask import Flask, render_template
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'C:\\Users\\Mark\\Desktop\\team_project\\e-voting\\tmp\\election.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select name, surname from candidate order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    curr = g.db.execute('select party_name,party_id from party order by party_id desc')
    parties = [dict(party_name=row[0], party_id=row[1]) for row in curr.fetchall()]
    return render_template('show_entries.html', entries=entries, parties=parties)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into candidate (name, surname, party_id, job, age, address) values (?, ?, ?, ?, ?, ?)',
                 [request.form['name'], request.form['surname'], request.form.get('party_id'), request.form['job'],
                  request.form['age'], request.form['address']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/add_party', methods=['POST'])
def add_party():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into party (party_name) values (?)',
                 [request.form['party_name']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('election.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    

        