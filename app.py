from comtypes import named_property
from flask import Flask, request, render_template, redirect, url_for, session, g, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
import pdfkit
import base64
from flask_wkhtmltopdf import Wkhtmltopdf

path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

app = Flask(__name__)
wkhtmltopdf = Wkhtmltopdf(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://openpg:openpgpwd@localhost:5432/FYP'
db = SQLAlchemy(app)
con_astr = 'postgresql://openpg:openpgpwd@localhost:5432/FYP'
dbb = create_engine(con_astr)
app.secret_key = os.urandom(24)
from classes.ProjectManager import ProjectManager
from classes.TeamLeader import TeamLeader


# ================================= Base64 Encoding =============================================


def get_image_file_as_base64_data():
    with open("C:/Users/Momin/Desktop/s8/fyptest2/static/Login/images/img-01.png", 'rb') as image_file:
        return base64.b64encode(image_file.read())


# ================================= Customer Analysis =============================================

@app.route('/customeranalysis', methods=['GET', 'POST'])
def customerAnalysis():
    print("Hello")
    from Functions import cust_pred
    cus_pred = cust_pred()
    return render_template('CustomerPrediction.html', cus_pred=cus_pred)


@app.route('/reportsform')
def reportsform():
    return render_template('report-form.html')
# ================================= Reports Generation =============================================

@app.route('/reports')
def reports():
    if g.auth == 1:
        if (session['role'] == "pm"):
            pm = ProjectManager(session['user'])
            result_set = pm.get_projects()

            from Functions import mps,get_portfolios
            projects= mps(1,1)
            portfolios= get_portfolios()

            portfoliosNprojects =[]
            portfolioslist =[]
            lstunique_portfolios=[]
            plist =[]

            p_MPS_list=[]
            for p in portfolios:
                portfoliosNprojects.append({"pf_name": p.portfolio_name, "p_name": p.project_name, "p_qty":p.qty})
                lstunique_portfolios.append({"pf_name": p.portfolio_name})
                # portfolioslist.append({"pf_name": p.portfolio_name})
                # plist.append({"p_name": p.project_name})

            for p in projects:
                p_MPS_list.append({"pf_name": p.portfolio_name, "p_name": p.project_name, "p_end_date":p.end_date, "p_qty":p.quantity})


            for p in p_MPS_list:
                for q in portfoliosNprojects:
                    if ((q.get('pf_name')==p.get("pf_name")) and (q.get('p_name')==p.get("p_name"))):
                        portfolioslist.append({"pf_name": q.get("pf_name"), "p_name": q.get("p_name"),
                                               "p_qty":p.get("p_qty"), "p_end_date":p.get("p_end_date")})

            # print(len(portfoliosNprojects))
            # print(len(p_MPS_list))
            print("+++++++++++++++++++++++ P F - L I S T+++++++++++++++++++++++++")
            print (portfolioslist)
            print("++++++++++++++++++++++++++++++++++++++++++++++++")

            unique_portfolios = set(val for dic in lstunique_portfolios for val in dic.values())
            lstunique_portfolios =list(unique_portfolios)
            print("UUUU++++++++++++++++++++++++++++++++++++++++++++++++")
            print(lstunique_portfolios)
            print(len(lstunique_portfolios))
            print("++++++++++++++++++++++++++++++++++++++++++++++++UUUU")


            print("+++++++++++++++++++++++ INDEXES +++++++++++++++++++++++++")
            # print(len(portfoliosNprojects))
            # for p in portfoliosNprojects:
            print(len(portfolioslist))
            for p in portfolioslist:
                print(p)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


            #mapping list of projects to their porfolios
            pjs=[[] for i in range(len(lstunique_portfolios))]
            qty=[[] for i in range(len(lstunique_portfolios))]
            endDates=[[] for i in range(len(lstunique_portfolios))]     #[Portfolios][project's End Dates]
            endDateNQty=[[] for i in range(len(lstunique_portfolios))]  #[endDate N Qty mapping]

            for pf in portfolioslist:
                for i in range(len(lstunique_portfolios)):
                    if pf.get('pf_name')==lstunique_portfolios[i]:
                        pjs[i].append(pf.get('p_name'))
                        qty[i].append(pf.get('p_qty'))
                        endDates[i].append(pf.get("p_end_date"))

            print("---------------P R O J S--------------------\n")
            print(pjs)
            print("---------------$$$$$$$$$--------------------\n")
            print(endDates)

           # print("+++++++++++++++++-++++---------------+++++++++++++++++++++++++++--------------------")
            # image = get_image_file_as_base64_data()
            # print("+++++++++++++++++-++++---------------+++++++++++++++++++++++++++--------------------")
            # print("+++++++++++++++++-++++---------------+++++++++++++++++++++++++++--------------------")
            # print(image)

            from datetime import datetime, timedelta

            dates = ["2016-12-10", "2018-01-07"]
            start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]

            print('----------------------------- Y E A R S ---------------------------------\n')

            yearHeaders=[]
            for i in range(start.year,end.year+1):
                yearHeaders.append(str(i))
            print (yearHeaders)


            print('----------------------------- D A T E S ---------------------------------\n')

            monthsInterval=dict(((start + timedelta(_)).strftime(r"%b-%y"),(start + timedelta(_)).strftime(r"%b")) for _ in range((end - start).days))
            monthsDecimal=dict(((start + timedelta(_)).strftime(r"%b-%y"),(start + timedelta(_)).strftime(r"%m")) for _ in range((end - start).days))
            print (monthsInterval)
            print(monthsDecimal)
            print('----------------------------- ! ! ! ! ! ---------------------------------\n')

            print(qty)

            monthsColSpan = []

            for year in yearHeaders:
                monthscount=0
                for key in monthsInterval.keys():
                    if key[4:6]==year[2:4]:
                        monthscount+=1
                monthsColSpan.append(monthscount)

            EDates=[[[]] for yy in range(len(yearHeaders))]                     #[years][months]
            for c1 in range(len(monthsColSpan)):
                    EDates[c1].extend([]for c2 in range (monthsColSpan[c1]-1))

            colcount=[]
            # print((str((endDates[0][1]).year))[2:-1])

            pfcounter=0

            for pf in endDates:  #list1 [[]]

                prcounter=0
                print("P F: ---------------------------------")
                print(pf)

                for pr in pf:                 #list2  []

                    print("P R: ---------------------------------")
                    print(pr)

                    TMcount = 0
                    Ycount = 0
                    for i in yearHeaders:
                        print("Y - C O U N T: ---------------------------------")
                        print(Ycount)
                        Mcount = 0

                        if str(pr.year)[2:4]==(i)[2:4]:                                                                 #YEAR COMPARISON

                            print("Y E A R : <><><><><><>---------------------------------")


                            for key, value in monthsDecimal.items():
                                print("\nM O N T H  C O M P A R I S O N : <><><><><><>---------------------------------")
                                print(str(pr.month) + '<=>' + value)
                                print("Y E A R  C O M P A R I S O N : <><><><><><>---------------------------------\n")
                                print(str(pr.year)[2:4] + '<=>' + key[4:6])
                                if (pr.month == int(value)) and (str(pr.year)[2:4]==key[4:6]):                          #MONTH COMPARISON
                                    print("M O N T H-----------------<><><><>---------------- Y E A R")
                                    print(str(pr.month) + ',' + value)
                                    print(str(pr.year) + ',' + key[4:6])
                                    print('ok')
                                    print('Mcount: ' + str(Mcount))
                                    print('Ycount: ' + str(Ycount))
                                    EDates[Ycount][Mcount].append(qty[pfcounter][prcounter])
                                    colcount.append(TMcount)                 # ROW x NO.of_COLUMNS + COLUMNS

                                print('Mcount: ' + str(Mcount))
                                if (str(pr.year)[2:4]==key[4:6]):
                                    Mcount+=1
                                TMcount+=1
                        print('Ycount: '+str(Ycount))
                        Ycount+=1
                    print('prcounter: ' + str(prcounter))
                    prcounter+=1
                print('pfcounter: ' + str(pfcounter))
                pfcounter+=1

            print(EDates)

            lc=0
            for i in range(len(EDates)):
                for j in range(len(EDates[i])):
                    lc+=len(EDates[i][j])

            print(lc)
            print(colcount)
            print(len(colcount))
            print('----------------------------- M O N T H S  I N  E A C H  Y E A R---------------------------------\n')

            print(monthsColSpan)

            css = ['C:\\Users\\Momin\\Desktop\\s8\\fyptest2\\static\\assets\\css\\paper-dashboard.css',
                   'C:\\Users\\Momin\\Desktop\\s8\\fyptest2\\static\\assets\\css\\bootstrap.min.css']
            options = {'orientation':'landscape',
                       'page-size':'A2'}

            rendered = render_template('reports.html', result_set=result_set, projects=projects,
                                       lstunique_portfolios=lstunique_portfolios, pjs=pjs, qty=qty,
                                       monthsInterval=monthsInterval, yearHeaders=yearHeaders,
                                       monthsColSpan=monthsColSpan, colcount=colcount, coliter=0)

            pdf = pdfkit.from_string(rendered, False, options=options, configuration=config, css=css)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
            return response

    # rendered=render_template('reports.html',name=name,loc=loc)
    # pdf= pdfkit.from_string(rendered, False, configuration=config)
    #
    # response=make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition']= 'inline; filename=output.pdf'
    # return response


# ================================= Functions for Projects =============================================

@app.route('/POrequest', methods=['GET', 'POST'])
def POrequest():
    if g.auth == 1:
        if (session['role'] == "pm"):
            resources = dbb.execute("SELECT resource_name FROM \"RESOURCES\" ")
            return render_template('request-PO.html', r_list=resources)
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
            c_proj = []
            ic_proj = []
            result_set = tl.get_projects()
            for p in result_set:
                if (len(tl.view_incompleted_dels(p.project_id)) > 0):
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
            pm = ProjectManager(session['user'])
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
        if (session['role'] == "pm"):
            pm = ProjectManager(session['user'])
            proid = request.form['proid']
            pname = request.form['pname']
            pdesc = request.form['pdesc']
            ppriority = request.form['ppriority']
            print("proid", proid)
            print("pname", pname)
            print("pdesc", pdesc)
            print("ppriority", ppriority)
            temp_list = []
            temp_list.append(pname)
            temp_list.append(pdesc)
            temp_list.append(ppriority)
            pm.edit_project(proid, temp_list)
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
            details = dbb.execute(
                "SELECT project_desc,issues,po_pending FROM \"PROJECTS\" where project_id=" + str(selected_proj))
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
        if (session['role'] == "pm"):
            result_set = dbb.execute("SELECT team_id FROM \"TEAMS\" ")
            if request.method == 'GET':
                return render_template('project-form.html', teams=result_set)
            else:
                if (request.form['submit'] == 'submit'):
                    pm = ProjectManager(session['user'])
                    proj_details = [request.form['project_name'], request.form['desc'], request.form['proj_type'],
                                    request.form['days_alloted'], request.form['priority'], request.form['team'],
                                    session['user']]
                    if pm.create_project(proj_details):
                        error = "New Project Created"
                        print(error)
                        return render_template('project-form.html', teams=result_set, error=error)
                    else:
                        error = "Failed to create new Project"
                        print(error)
                        return render_template('project-form.html', teams=result_set, error=error)
                elif request.form['submit'] == 'analyze':
                    from Functions import predict
                    proj_details = [request.form['project_name'], request.form['desc'], request.form['proj_type'],
                                    request.form['days_alloted'], request.form['priority'], request.form['team'],
                                    session['user']]
                    prediction = predict(proj_details);
                    return render_template('Analyze.html', proj_details=proj_details, prediction=prediction)
                else:
                    return render_template('project-form.html', teams=result_set)
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
        if (session['role'] == "pm"):
            pm = ProjectManager(session['user'])
            if ctype == "comment":
                pm.add_comment(proid, session['user'], cdesc)
            else:
                pm.report_issue(proid, session['user'], cdesc)
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
    if g.auth == 1:
        selected_proj = request.form['proid']
        # print("proj id", selected_proj)
        pm = ProjectManager(session['user'])
        # print(pm.username)
        dels = pm.get_deliverables(selected_proj)  # type: object
        proj_comments = pm.view_comments(selected_proj)
        print(proj_comments)
        final_del = []
        final_comments = []
        for d in dels:
            final_del.append(
                {"del_id": d.del_id, "project_id": d.project_id, "del_name": d.del_name, "del_desc": d.del_desc,
                 "priority": d.priority})
        for c in proj_comments:
            final_comments.append({"username": c.username, "comment": c.comment})
        print(final_comments)
        if selected_proj:
            return jsonify({'proid': [row for row in final_del], 'commnt': [comment for comment in final_comments]})
        return jsonify({'error': 'Missing data!'})

    else:
        return render_template('ERROR404.html')


@app.route('/getDel_Editdetails', methods=['POST'])
def getDel_Editdetails():
    if g.auth == 1:
        if (session['role'] == "tl"):
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
            tl = TeamLeader(session['user'])
            proid = request.form['proid']
            delid = request.form['delid']
            pname = request.form['pname']
            pdesc = request.form['pdesc']
            ppriority = request.form['ppriority']
            ls = []
            ls.append(pname)
            ls.append(pdesc)
            ls.append(ppriority)
            print("delid", delid)
            print("proid", proid)
            print("pname", pname)
            print("pdesc", pdesc)
            print("ppriority", ppriority)
            tl.edit_deliverable(delid, ls)
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
        if (session['role'] == "tl"):
            tl = TeamLeader(session['user'])
            selected_proj = request.form['proid']
            session['proid'] = selected_proj
            print("proj id", selected_proj)
            delsComp = tl.view_completed_dels(selected_proj)
            print(delsComp)
            delsIncomp = tl.view_incompleted_dels(selected_proj)
            print(delsIncomp)
            members = tl.get_members()

            if selected_proj:
                return render_template('deliverables_leader.html', delsComp=delsComp, delsIncomp=delsIncomp,
                                       projid=selected_proj, members=members)
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


@app.route('/formfilling2', methods=['GET', 'POST'])
def formfilling2():
    if g.auth == 1:
        if (session['role'] == "tl"):
            if request.method == 'GET':
                return render_template('del-form.html')
            else:
                tl = TeamLeader(session['user'])
                del_details = [request.form['del_name'], request.form['desc'], request.form['priority']]
                if tl.create_deliverable(session['proid'], del_details):
                    error = "New Deliverable Created"
                    print(error)
                    return render_template('del-form.html', error=error)
                else:
                    error = "Failed to create new Deliverable"
                    print(error)
                    return render_template('del-form.html', error=error)
        else:
            render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


@app.route('/submitproject', methods=['POST'])
def submitproj():
    if g.auth == 1:
        if (session['role'] == "tl"):
            tl = TeamLeader(session['user'])
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
        proid = request.form['proid']
        delid = request.form['delid']
        activityid = request.form['activityid']
        ctitle = request.form['ctitle']
        cdesc = request.form['cdesc']
        ctype = request.form['ctype']
        # print("delid", delid)
        # print("activityid", activityid)
        # print("proid", proid)
        # print("ctitle", ctitle)
        # print("cdesc", cdesc)
        # print("ctype", ctype)
        if (session['role'] == 'tl'):
            tl = TeamLeader(session['user'])
            if ctype == "Simple":
                tl.add_comment(proid, delid, activityid, session['user'], cdesc)
            else:
                tl.report_issuex(proid, delid, activityid, session['user'], cdesc)
        if proid:
            return jsonify({'success': 'Yahoo'})
        return jsonify({'error': 'Missing data!'})
    else:
        return render_template('ERROR404.html')


@app.route('/getactivities', methods=['POST'])
def getactivities():
    if g.auth == 1:
        if session['role'] == "tl":
            tl = TeamLeader(session['user'])
            selected_proj = request.form['proid']
            seleted_del = request.form['delid']
            print("proj id", selected_proj)
            activities = tl.get_activities(selected_proj, seleted_del)
            final_activities = []
            for a in activities:
                final_activities.append(
                    {"activity_id": a.activity_id, "activity_name": a.activity_name, "project_id": a.project_id,
                     "start_date": a.start_date, "end_date": a.end_date, "days_alloted": a.days_alloted,
                     "del_id": a.del_id, "priority": a.priority, "username": a.username, "status": a.status})
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
    ls = []
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
        tl = TeamLeader(session['user'])
        tl.edit_activity(activityid, ls)
    # dbb.execute('UPDATE "PROJECTS" SET phase = \'dONE\' where project_id='+str(selected_proj))  # type: object
    if proid:
        return jsonify({'success': 'Yahoo'})
    return jsonify({'error': 'Missing data!'})


@app.route('/approveActivity', methods=['POST'])
def approveActivity():
    if g.auth == 1:
        if session['role'] == "tl":
            tl = TeamLeader(session['user'])
            proid = request.form['proid']
            delid = request.form['delid']
            activityid = request.form['activityid']
            print("approve activity")
            print("delid", delid)
            print("activityid", activityid)
            print("proid", proid)
            tl.approve_activity(proid, delid, activityid)
            # dbb.execute('UPDATE "PROJECTS" SET phase = \'dONE\' where project_id='+str(selected_proj))  # type: object
            if proid:
                return jsonify({'success': 'Yahoo'})
            return jsonify({'error': 'Missing data!'})
        else:
            return render_template('ERROR404.html')
    else:
        return render_template('ERROR404.html')


# =====================================================================================================================


@app.route('/dashboard', methods=['GET', 'POST'])
def view_dashboard():
    from Functions import get_allocated_fund
    allocatedfunds = []
    releasedfunds = [1234, 1234]
    if g.auth == 1:
        if (session['role'] == "pm"):
            # ============================= total issues =================================
            current_user = session['user']
            pm = ProjectManager(current_user)
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
                allocatedfunds.insert(0, get_allocated_fund(proj.project_id))
                issues.insert(0, i)
                _list.insert(0, i)
                _listProjnames.insert(0, n)
                _listAllotedDays.insert(0, d)

                count = count + 1
            total_issues = sum(_list)
            total_funds = (int)(sum(allocatedfunds) / 1000000)
            total_funds = str(total_funds) + 'M'
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
            return render_template('Dashboard.html', allocatedfunds=allocatedfunds, releasedfunds=releasedfunds,
                                   total_issues=total_issues, live_projects=p,
                                   _listProjnames=_listProjnames, issues=issues,
                                   _listAllotedDays=_listAllotedDays, total_projs=t, auth=session['role'],
                                   total_funds=total_funds)

        elif (session['role'] == "tl"):
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
            total_issues = (int)(sum(allocatedfunds) / 1000000)
            total_issues = str(total_issues) + 'M'
            # =============================================================================

            # ============================= total Live Projects =================================
            p = 0
            t = 0
            for proj in projects:
                if proj.status != 'Completed':
                    p += 1
                t += 1
            # =============================================================================

            team_members = tl.get_members()
            print(_listProjnames)
            print(_listAllotedDays)
            return render_template('dashboard_leader.html', total_issues=total_issues, live_projects=p,
                                   allocatedfunds=allocatedfunds,
                                   _listProjnames=_listProjnames, releasedfunds=releasedfunds,
                                   _listAllotedDays=_listAllotedDays, total_projs=t, auth=session['role'],
                                   team_members=team_members)
    else:
        return render_template('ERROR404.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    from Functions import user_verification
    if request.method == 'POST':
        session.pop('user', None)
        user = user_verification(request.form['email'], request.form['pass'])
        if (user):
            session['user'] = user.username
            print(session['user'])
            if (user.role == "Project Manager"):
                g.current_user = ProjectManager(user.username)
                session['role'] = "pm"
                print("Valid User")
                return redirect(url_for('view_dashboard'))
            elif (user.role == "Team Leader"):
                session['role'] = "tl"
                print("Valid User")
                return redirect(url_for('view_dashboard'))
            else:
                error = 'Not enough privileges'
                return render_template('Login.html', error=error)
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('Login.html', error=error)
    return render_template('Login.html')


@app.before_request
def before_request():
    if 'user' in session:
        g.auth = 1
        print("in session ")
    else:
        g.auth = 0
        print("no session ")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
