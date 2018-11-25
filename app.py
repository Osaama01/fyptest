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

# @app.route('/projects', methods=['GET', 'POST'])
# def projects():
#     if g.auth == 1:
#         pm = ProjectManager(session['user'])
#         result_set = pm.get_projects()
#         # for i in result_set:
#         #     print(i)
#         return render_template('projects.html', result_set=result_set)
#     else:
#         return render_template('ERROR404.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if g.auth == 1:
        tl = TeamLeader('akinson7j')
        result_set = tl.get_projects()
        # for i in result_set:
        #     print(i)
        return render_template('projects_leader.html', result_set=result_set)
    else:
        return render_template('ERROR404.html')

@app.route('/closeproject', methods=['POST'])
def closeproj():
    from models.DELIVERABLES import DELIVERABLES
    selected_proj = request.form['p_id']
    print("proj id", selected_proj)
    dbb.execute('UPDATE "PROJECTS" SET phase = \'dONE\' where project_id='+str(selected_proj))  # type: object
    print('Yahoo')
    if selected_proj:
        return jsonify({'success': 'Yahoo'})
    return jsonify({'error': 'Missing data!'})

@app.route('/getdeliverables', methods=['POST'])
def process():
    from models.DELIVERABLES import DELIVERABLES
    selected_proj = request.form['proid']
    # print("proj id", selected_proj)
    pm=ProjectManager(session['user'])
    # print(pm.username)
    dels = pm.get_deliverables(selected_proj) # type: object
    proj_comments=pm.view_comments(selected_proj)
    print(proj_comments)
    final_del=[]
    final_comments=[]
    for d in dels:
        final_del.append({"del_id" : d.del_id,"project_id" : d.project_id,"del_name" : d.del_name,"del_desc" : d.del_desc,"priority" : d.priority})
    for c in proj_comments:
         final_comments.append({"username" : c.username,"comment" : c.comment})
    # print(final_comments)
    if selected_proj:
        return jsonify({'proid': [row for row in final_del], 'commnt': [comment for comment in final_comments]})
    return jsonify({'error': 'Missing data!'})

@app.route('/getactivities', methods=['POST'])
def getactivities():

    selected_proj = request.form['proid']
    seleted_del = request.form['delid']
    print("proj id", selected_proj)
    activities = dbb.execute('SELECT * FROM \"ACTIVITIES\" where project_id='+str(selected_proj)+'and del_id='+str(seleted_del
                                                                                                             ))  # type: object
    print('Fetching Activities')
    if selected_proj:
        return jsonify({'activities': [dict(row) for row in activities]})

    return jsonify({'error': 'Missing data!'})

@app.route('/getProj_Editdetails', methods=['POST'])
def pEditdetails():
    from Functions import get_project_edit_details
    selected_proj = request.form['p_id']
    print("proj id", selected_proj)
    details = get_project_edit_details(selected_proj)
    if selected_proj:
        return jsonify({'PeditDet': [dict(row) for row in details]})

    return jsonify({'error': 'Missing data!'})

@app.route('/getDel_Editdetails', methods=['POST'])
def dEditdetails():
    from Functions import get_del_edit_details
    selected_del = request.form['del_id']
    selected_proj = request.form['proj']
    print("del id", selected_del)
    details = get_del_edit_details(selected_proj,selected_del)
    if selected_del:
        return jsonify({'DeditDet': [dict(row) for row in details]})

    return jsonify({'error': 'Missing data!'})

@app.route('/projects/leader_deliverables', methods=['POST'])
def leader_deliverables():
    from models.DELIVERABLES import DELIVERABLES
    tl = TeamLeader('akinson7j')
    selected_proj = request.form['proid']
    print("proj id", selected_proj)
    delsComp = tl.view_completed_dels(selected_proj)
    print(delsComp)
    delsIncomp = tl.view_incompleted_dels(selected_proj)
    print(delsIncomp)

    if selected_proj:
        return render_template('deliverables_leader.html', delsComp=delsComp, delsIncomp=delsIncomp, projid=selected_proj)

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
            pm = ProjectManager(session['user'])
            proj_details=[request.form['project_name'],request.form['desc'],request.form['proj_type'],request.form['days_alloted'],request.form['priority'],request.form['team'],session['user']]
            if pm.create_project(proj_details):
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
        if(session['role'] == "pm"):
            # ============================= total issues =================================
            current_user=session['user']
            pm=ProjectManager(current_user)
            projects = pm.get_projects()
            _list = []
            _listProjnames = []
            _listAllotedDays = []
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

        elif(session['role'] == "tl"):
            # ============================= total issues =================================
            current_user = session['user']
            tl = TeamLeader(current_user)
            projects = tl.get_projects()
            _list = []
            _listProjnames = []
            _listAllotedDays = []
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
                session['role']="pm"
                print("Valid User")
                return redirect(url_for('view_dashboard'))
            elif(user.role=="Team Leader"):
                session['role']="tl"
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
