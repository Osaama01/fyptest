from flask import Flask,request,render_template,redirect,url_for,session,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://openpg:1234@localhost:5432/fyp'
str='postgresql://openpg:1234@localhost:5432/fyp'
db=SQLAlchemy(app)
dbb=create_engine(str)
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
        result_set = dbb.execute("SELECT team_id FROM \"TEAMS\" ")
        if request.method=='GET':
            return render_template('project-form.html',teams=result_set)
        else:
            from Functions import create_project
            proj_details=[request.form['project_name'],request.form['desc'],request.form['proj_type'],request.form['days_alloted'],request.form['priority'],request.form['team'],session['user']]
            if create_project(proj_details):
                error="New Project Created"
                print (error)
                return render_template('project-form.html', teams=result_set, error=error)
            else:
                error = "Failed to create new Project"
                print (error)
                return render_template('project-form.html', teams=result_set, error=error)
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

    from classes.ProjectManager import ProjectManager
    pm=ProjectManager("gtour90")
    pmlist=pm.view_projects()
    for p in pmlist:
        print (p.deliverables)
        dels=p.deliverables
        for d in dels:
            print (d.Activities)
    return "hello"
    # from Functions import user_verification
    # if request.method == 'POST':
    #     session.pop('user',None)
    #     user=user_verification(request.form['email'], request.form['pass'])
    #     if(user):
    #         session['user']=user.username
    #         print(session['user'])
    #         if(user.role=="Project Manager"):
    #             print("Valid User")
    #             return redirect(url_for('view_dashboard'))
    #         else:
    #             error = 'Not enough privileges'
    #             return render_template('Login.html', error=error)
    #     else:
    #         error='Invalid Credentials. Please try again.'
    #         return render_template('Login.html',error=error)
    # return render_template('Login.html')


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
