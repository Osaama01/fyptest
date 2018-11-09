from flask import Flask,request,render_template,redirect,url_for,session,g
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://openpg:1234@localhost:5432/fyp'
db=SQLAlchemy(app)
app.secret_key = os.urandom(24)

#from models.USERS import USERS
# @app.route('/formfilling', methods=['GET', 'POST'])
# def formfilling():
#     if request.method == 'POST':
#         new_user=USERS(request.form['username'],request.form['password'],request.form['first_name'],request.form['last_name'],request.form['dob'],request.form['role'])
#         db.session.add(new_user)
#         db.session.commit()
#         return ("Success")
#         # else:
#         #     return "Failed"
#     return render_template('Formfilling.html')

@app.route('/formfilling1', methods=['GET', 'POST'])
def formfilling1():
    if g.auth == 1:
        from models.TEAMS import TEAMS
        teams=TEAMS.query.all();
        return render_template('project-form.html')
    else:
        return render_template('ERROR404.html')



@app.route('/dashboard',methods=['GET', 'POST'])
def view_dashboard():
    if g.auth==1:
        return render_template('Dashboard.html')
    else:
        return render_template('ERROR404.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    from Functions import user_verification
    if request.method == 'POST':
        session.pop('user',None)
        user=user_verification(request.form['email'], request.form['pass'])
        if(user):
            session['user']=user.username
            print(session['user'])
            if(user.role=="Project Manager"):
                print("Valid User")
                return redirect(url_for('view_dashboard'))
            else:
                error = 'Not enough privileges'
                return render_template('Login.html', error=error)
        else:
            error='Invalid Credentials. Please try again.'
            return render_template('Login.html',error=error)
    return render_template('Login.html')


@app.before_request
def before_request():
        if 'user' in session:
            g.auth=1
            print("in session ")
        else:
            g.auth=0
            print("no session ")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run()
