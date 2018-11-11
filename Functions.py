from models.USERS import USERS
from app import dbb
from app import db
import datetime

def user_verification(p_username,p_password):
    print (p_username)
    user = USERS.query.filter_by(username=p_username).first()
    if user:
        print("Success")
        if user.password == p_password:
            print(user.role)
            return user
        else:
            print("Invalid Password")
            return False
    else:
        print("Wrong Username")
        return False

def create_project(details_list):
    from models.PROJECTS import PROJECTS
    try:
        result_set = dbb.execute("SELECT MAX(project_id) FROM \"PROJECTS\"") #Project id for new project
        for r in result_set:
            project_id=r[0]+1
        new_proj=PROJECTS(project_id,details_list[0],details_list[1],details_list[2],None,None,details_list[3],"In Process","Initiation",details_list[4],1,details_list[5],0,0,details_list[6])
        db.session.add(new_proj)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def get_project_list(username):
    from models.PROJECTS import PROJECTS
    projects=PROJECTS.query.filter_by(username=username).all()
    for p in projects:
        p.set()
    return projects

def get_project(project_id):
    from models.PROJECTS import PROJECTS
    proj=PROJECTS.query.filter_by(project_id=project_id).first()
    proj.set()
    return proj


def get_del_list(project_id):
    from models.DELIVERABLES import DELIVERABLES
    deliverables=DELIVERABLES.query.filter_by(project_id=project_id).all()
    for d in deliverables:
        d.set()
    return deliverables

def get_del(del_id):
    from models.DELIVERABLES import DELIVERABLES
    deliverable=DELIVERABLES.query.filter_by(del_id=del_id).first()
    deliverable.set()
    return deliverable

def get_activities(del_id):
    from models.ACTIVITIES import ACTIVITIES
    activities=ACTIVITIES.query.filter_by(del_id=del_id).all()
    return activities

def get_allocated_fund(project_id):
    from models.FINANCES import FINANCES
    allocated_fund=FINANCES.query.with_entities(FINANCES.allocation).filter_by(project_id=project_id).first()
    return allocated_fund[0]

def get_POs(project_id):
    from models.PO import PO
    PO_list=PO.query.with_entities(PO.r_id,PO.quantity,PO.status).filter_by(project_id=project_id).all()
    return PO_list
