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
            project_id=r[0]
        new_proj=PROJECTS(project_id,details_list[0],details_list[1],details_list[2],None,None,details_list[3],"In Process","Initiation",details_list[4],1,details_list[5],0,0,details_list[6])
        db.session.add(new_proj)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False




