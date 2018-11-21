from flask import Flask,request,render_template,redirect,url_for,session,g,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://openpg:1234@localhost:5432/fyp'
con_str='postgresql://openpg:1234@localhost:5432/fyp'
db=SQLAlchemy(app)
dbb=create_engine(con_str)
app.secret_key = os.urandom(24)
from classes.ProjectManager import ProjectManager
from classes.TeamLeader import TeamLeader


@app.route('/POrequest', methods=['GET', 'POST'])
def POrequest():
    if g.auth == 1:
        resources=dbb.execute("SELECT resource_name FROM \"RESOURCES\" ")
        return render_template('request-PO.html',r_list=resources)
    else:
        return render_template('ERROR404.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if g.auth == 1:
        pm = ProjectManager(session['user'])
        result_set = pm.get_projects()
        # for i in result_set:
        #     print(i)
        return render_template('projects.html', result_set=result_set)
    else:
        return render_template('ERROR404.html')

@app.route('/getdeliverables', methods=['POST'])
def process():
    from models.DELIVERABLES import DELIVERABLES
    selected_proj = request.form['pid']
    print("proj id", selected_proj)
    pm=ProjectManager(session['user'])
    print(pm.username)
    dels = pm.get_deliverables(selected_proj) # type: object
    final_del=[]
    for d in dels:
        final_del.append({"del_id" : d.del_id,"project_id" : d.project_id,"del_name" : d.del_name,"del_desc" : d.del_desc,"priority" : d.priority})
    if selected_proj:
        return jsonify({'pid': [row for row in final_del]})

    return jsonify({'error': 'Missing data!'})


@app.route('/getPdetails', methods=['POST'])
def pdetails():
    selected_proj = request.form['pid']
    print("proj id", selected_proj)
    details = dbb.execute("SELECT project_desc,issues,po_pending FROM \"PROJECTS\" where project_id=" + str(selected_proj))
    if selected_proj:
        return jsonify({'pdet': [dict(row) for row in details]})

    return jsonify({'error': 'Missing data!'})


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
        from models.PROJECTS import PROJECTS
        # ============================= total issues =================================
        # projects = PROJECTS.query.all()

        current_user=session['user']
        pm=ProjectManager(current_user)
        projects = pm.get_projects()
        # abc=db.engine.execute('select * from "PROJECTS" where username="sgoad9l"');
        _list = []
        _listProjnames = []
        _listAllotedDays = []
        # db.engine.execute("select days_alloted from PROJECTS where username='sgoad9l'")
        count = 0
        for proj in projects:
            i = proj.issues
            n = proj.project_name
            d = proj.days_alloted
            _list.insert(0, i)

            if count < 20:
                _listProjnames.insert(0, n)
                _listAllotedDays.insert(0, d)

            count = count + 1
        total_issues = sum(_list)
        # =============================================================================

        # ============================= total Live Projects =================================
        p = 0
        t = 0
        for proj in projects:
            if proj.status != 'Completed':
                p += 1
            t += 1
        # =============================================================================
        print(_listProjnames)
        print(_listAllotedDays)
        return render_template('dashboard.html', total_issues=total_issues, live_projects=p,
                               _listProjnames=_listProjnames,
                               _listAllotedDays=_listAllotedDays, total_projs=t)
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
