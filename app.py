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



# ================================= Functions for Projects =============================================

@app.route('/POrequest', methods=['GET', 'POST'])
def POrequest():
    if g.auth == 1:
        if(session['role'] == "pm"):
            resources=dbb.execute("SELECT resource_name FROM \"RESOURCES\" ")
            return render_template('request-PO.html',r_list=resources)
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

# @app.route('/projects', methods=['GET', 'POST'])

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if g.auth == 1:
        if (session['role'] == "pm"):
            pm = ProjectManager(session['user'])
            result_set = pm.get_projects()
            # for i in result_set:
            #     print(i)
            return render_template('projects.html', result_set=result_set)

        elif (session['role'] == "tl"):
            tl = TeamLeader(session['user'])
            c_proj=[]
            ic_proj=[]
            result_set = tl.get_projects()
            for p in result_set:
                if(len(tl.view_incompleted_dels(p.project_id))> 0):
                    ic_proj.append(p)
                else:
                    c_proj.append(p)
            # for i in result_set:
            #     print(i)
            return render_template('projects_leader.html', c_proj=c_proj, ic_proj=ic_proj)

        else:
            return render_template('ERROR404.html')

    else:
        return render_template('ERROR404.html')

# @app.route('/projects', methods=['GET', 'POST'])
# def projects():
#     if g.auth == 1:
#         tl = TeamLeader('akinson7j')
#         result_set = tl.get_projects()
#         # for i in result_set:
#         #     print(i)
#         return render_template('projects_leader.html', result_set=result_set)
#     else:
#         return render_template('ERROR404.html')

@app.route('/closeproject', methods=['POST'])
def closeproj():
    if g.auth == 1:
        if (session['role'] == "pm"):
            pm=ProjectManager(session['user'])
            selected_proj = request.form['p_id']
            print("proj id", selected_proj)
            pm.close_project(selected_proj)
            print('Yahoo')
            if selected_proj:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


@app.route('/confirmEditProj', methods=['POST'])
def editproj():
    if g.auth == 1:
        if(session['role'] == "pm"):
            pm = ProjectManager(session['user'])
            proid=request.form['proid']
            pname=request.form['pname']
            pdesc=request.form['pdesc']
            ppriority=request.form['ppriority']
            print("proid", proid)
            print("pname", pname)
            print("pdesc", pdesc)
            print("ppriority", ppriority)
            temp_list=[]
            temp_list.append(pname)
            temp_list.append(pdesc)
            temp_list.append(ppriority)
            pm.edit_project(proid,temp_list)
            if proid:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

@app.route('/getProj_Editdetails', methods=['POST'])
def getProj_Editdetails():
    if g.auth == 1:
        if (session['role'] == "pm"):
            from Functions import get_project_edit_details
            selected_proj = request.form['p_id']
            print("proj id", selected_proj)
            details = get_project_edit_details(selected_proj)
            if selected_proj:
                return jsonify({'PeditDet': [dict(row) for row in details]})

            return jsonify({'error': 'Missing data!'})
        else:
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

@app.route('/getPdetails', methods=['POST'])
def getPdetails():
    if g.auth == 1:
        if (session['role'] == "pm"):
            selected_proj = request.form['pid']
            print("proj id", selected_proj)
            details = dbb.execute("SELECT project_desc,issues,po_pending FROM \"PROJECTS\" where project_id=" + str(selected_proj))
            if selected_proj:
                return jsonify({'pdet': [dict(row) for row in details]})

            return jsonify({'error': 'Missing data!'})
        else:
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


@app.route('/formfilling1', methods=['GET', 'POST'])
def formfilling1():
    if g.auth == 1:
        if(session['role'] == "pm"):
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
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


@app.route('/submitProjcomment', methods=['POST'])
def submitProjcomment():
    if g.auth == 1:
        proid = request.form['proid']
        ctitle = request.form['ctitle']
        cdesc = request.form['cdesc']
        ctype = request.form['ctype']
        print("proid", proid)
        print("ctitle", ctitle)
        print("cdesc", cdesc)
        print("ctype", ctype)
        if(session['role'] == "pm"):
            pm = ProjectManager(session['user'])
            if ctype == "comment":
                pm.add_comment(proid,session['user'],cdesc)
            else:
                pm.report_issue(proid,session['user'],cdesc)
            if proid:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})

        elif (session['role'] == "tl"):
            tl = TeamLeader(session['user'])
            if ctype == "comment":
                tl.add_comment(proid, session['user'], cdesc)
            else:
                tl.report_issue(proid, session['user'], cdesc)
            if proid:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

# ================================= Functions for Deliverables =============================================


@app.route('/getdeliverables', methods=['POST'])
def process():
    if g.auth== 1:
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
            print(final_comments)
            if selected_proj:
                return jsonify({'proid': [row for row in final_del], 'commnt': [comment for comment in final_comments]})
            return jsonify({'error': 'Missing data!'})

    else:
        return render_template('ERROR404.html')

@app.route('/getDel_Editdetails', methods=['POST'])
def getDel_Editdetails():
    if g.auth == 1:
        if(session['role'] == "tl"):
            from Functions import get_del_edit_details
            # final_dellist=[]
            selected_del = request.form['delid']
            selected_proj = request.form['proj']
            print("del id", selected_del)
            details = get_del_edit_details(selected_proj, selected_del)
            # final_dellist.append({"del_name" : details.del_name,"del_desc" : details.del_desc ,"priority" : details.priority})
            # print(final_dellist)
            if selected_del:
                return jsonify({'DeditDet': [dict(row) for row in details]})

            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

@app.route('/confirmEditDel', methods=['POST'])
def confirmEditDel():
    if g.auth == 1:
        if session['role'] == "tl":
            tl=TeamLeader(session['user'])
            proid = request.form['proid']
            delid = request.form['delid']
            pname = request.form['pname']
            pdesc = request.form['pdesc']
            ppriority = request.form['ppriority']
            ls=[]
            ls.append(pname)
            ls.append(pdesc)
            ls.append(ppriority)
            print("delid", delid)
            print("proid", proid)
            print("pname", pname)
            print("pdesc", pdesc)
            print("ppriority", ppriority)
            tl.edit_deliverable(delid,ls)
            # dbb.execute('UPDATE "PROJECTS" SET phase = \'dONE\' where project_id='+str(selected_proj))  # type: object
            if proid:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

@app.route('/projects/leader_deliverables', methods=['POST'])
def leader_deliverables():
    if g.auth == 1:
        if(session['role'] == "tl"):
            tl = TeamLeader(session['user'])
            selected_proj = request.form['proid']
            print("proj id", selected_proj)
            delsComp = tl.view_completed_dels(selected_proj)
            print(delsComp)
            delsIncomp = tl.view_incompleted_dels(selected_proj)
            print(delsIncomp)
            members=tl.get_members()

            if selected_proj:
                return render_template('deliverables_leader.html', delsComp=delsComp, delsIncomp=delsIncomp, projid=selected_proj,members=members)
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

@app.route('/formfilling2', methods=['GET', 'POST'])
def formfilling2():
    if g.auth == 1:
        if(session['role'] == "tl"):
            if request.method=='GET':
                return render_template('del-form.html')
            else:
                tl = TeamLeader(session['user'])
                del_details=[request.form['del_name'],request.form['desc'],session['user']]
                if tl.create_deliverable(123,del_details):
                    error="New Deliverable Created"
                    print (error)
                    return render_template('project-form.html',error=error)
                else:
                    error = "Failed to create new Deliverable"
                    print (error)
                    return render_template('project-form.html', error=error)
        else:
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


@app.route('/submitproject', methods=['POST'])
def submitproj():
    if g.auth == 1:
        if (session['role'] == "tl"):
            tl=TeamLeader(session['user'])
            selected_proj = request.form['p_id']
            print("proj id", selected_proj)
            tl.mark_completed(selected_proj)
            print('Yahoo')
            if selected_proj:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

# ================================= Functions for Activity =============================================


@app.route('/submitActivitycomment', methods=['POST'])
def submitActivitycomment():
    if g.auth == 1:
        proid=request.form['proid']
        delid=request.form['delid']
        activityid=request.form['activityid']
        ctitle=request.form['ctitle']
        cdesc=request.form['cdesc']
        ctype=request.form['ctype']
        # print("delid", delid)
        # print("activityid", activityid)
        # print("proid", proid)
        # print("ctitle", ctitle)
        # print("cdesc", cdesc)
        # print("ctype", ctype)
        if(session['role'] == 'tl'):
            tl=TeamLeader(session['user'])
            if ctype == "Simple":
                tl.add_comment(proid,delid,activityid,session['user'],cdesc)
            else:
                tl.report_issuex(proid,delid,activityid,session['user'],cdesc)
        if proid:
            return jsonify({'success': 'Yahoo'})
        return jsonify({'error': 'Missing data!'})
    else:
        return render_template('ERROR404.html')

@app.route('/getactivities', methods=['POST'])
def getactivities():
    if g.auth == 1:
        if session['role'] == "tl":
            tl=TeamLeader(session['user'])
            selected_proj = request.form['proid']
            seleted_del = request.form['delid']
            print("proj id", selected_proj)
            activities =tl.get_activities(selected_proj,seleted_del)
            final_activities=[]
            for a in activities:
                final_activities.append({"activity_id" : a.activity_id,"activity_name" : a.activity_name,"project_id" : a.project_id,"start_date" : a.start_date,"end_date" : a.end_date,"days_alloted" : a.days_alloted,"del_id" : a.del_id,"priority" : a.priority,"username" : a.username,"status" : a.status})
            print('Fetching Activities')
            if selected_proj:
                return jsonify({'activities': [row for row in final_activities]})

            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')

@app.route('/confirmEditActivity', methods=['POST'])
def confirmEditActivity():
    proid = request.form['proid']
    delid = request.form['delid']
    activityid = request.form['activityid']
    activityname = request.form['activityname']
    activityassto = request.form['activityassto']
    activitypriority = request.form['activitypriority']
    ls=[]
    ls.append(activityname)
    ls.append(activitypriority)
    ls.append(activityassto)
    print("delid", delid)
    print("activityid", activityid)
    print("proid", proid)
    print("activityname", activityname)
    print("activityassto", activityassto)
    print("activitypriority", activitypriority)
    if session['role'] == "tl":
        tl=TeamLeader(session['user'])
        tl.edit_activity(activityid,ls)
    # dbb.execute('UPDATE "PROJECTS" SET phase = \'dONE\' where project_id='+str(selected_proj))  # type: object
    if proid:
        return jsonify({'success': 'Yahoo'})
    return jsonify({'error': 'Missing data!'})


@app.route('/approveActivity', methods=['POST'])
def approveActivity():
    if g.auth == 1:
        if session['role'] == "tl":
            tl=TeamLeader(session['user'])
            proid=request.form['proid']
            delid=request.form['delid']
            activityid=request.form['activityid']
            print("approve activity")
            print("delid", delid)
            print("activityid", activityid)
            print("proid", proid)
            tl.approve_activity(proid,delid,activityid)
            # dbb.execute('UPDATE "PROJECTS" SET phase = \'dONE\' where project_id='+str(selected_proj))  # type: object
            if proid:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')




# =====================================================================================================================




@app.route('/dashboard',methods=['GET', 'POST'])
def view_dashboard():
    from Functions import get_allocated_fund
    allocatedfunds = []
    releasedfunds = [1234, 1234]
    if g.auth==1:
        if(session['role'] == "pm"):
            # ============================= total issues =================================
            current_user=session['user']
            pm=ProjectManager(current_user)
            projects = pm.get_projects()
            _list = []
            _listProjnames = []
            _listAllotedDays = []

            issues = []
            count = 0
            for proj in projects:
                i = proj.issues
                # allocatedfunds.append(get_allocated_fund(proj.project_id))
                n = proj.project_name
                d = proj.days_alloted
                allocatedfunds.insert(0,get_allocated_fund(proj.project_id))
                issues.insert(0, i)
                _list.insert(0, i)
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
            return render_template('Dashboard.html', allocatedfunds=allocatedfunds, releasedfunds=releasedfunds, total_issues=total_issues, live_projects=p,
                                   _listProjnames=_listProjnames,issues=issues,
                                   _listAllotedDays=_listAllotedDays, total_projs=t,auth=session['role'])

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
                allocatedfunds.insert(0, get_allocated_fund(proj.project_id))
                d = proj.days_alloted
                _list.insert(0, i)
                _listProjnames.insert(0, n)
                _listAllotedDays.insert(0, d)
                count = count + 1
            total_issues = (int)(sum(allocatedfunds)/1000000)
            total_issues=str(total_issues)+'M'
            # =============================================================================

            # ============================= total Live Projects =================================
            p = 0
            t = 0
            for proj in projects:
                if proj.status != 'Completed':
                    p += 1
                t += 1
            # =============================================================================

            team_members=tl.get_members()
            print(_listProjnames)
            print(_listAllotedDays)
            return render_template('dashboard_leader.html', total_issues=total_issues, live_projects=p,allocatedfunds=allocatedfunds,
                                   _listProjnames=_listProjnames,releasedfunds=releasedfunds,
                                   _listAllotedDays=_listAllotedDays, total_projs=t,auth=session['role'],team_members=team_members)
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
                g.current_user=ProjectManager(user.username)
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
