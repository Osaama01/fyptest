from models.USERS import USERS
from cryptography.fernet import Fernet
from app import dbb

def user_verification(p_username,p_password):
    print (p_username)
    user = USERS.query.filter_by(username=p_username).first()
    if user:
        print("Success")
        if decode(user.password) == p_password:
            print(user.role)
            return user
        else:
            print("Invalid Password")
            return False
    else:
        print("Wrong Username")
        return False

def encode(password):
    cipher_suite = Fernet(b'nIoDjdsM388MiEbvlAo3LVpbPeLME5uDEovGH_kXKFg=')
    cipher_text = cipher_suite.encrypt((password).encode('UTF-8'))
    cipher_text_final = cipher_suite.encrypt((cipher_text.decode('UTF-8')).encode('UTF-8'))
    cipher_text_final=cipher_text_final.decode('UTF-8')
    # print(cipher_text_final)
    return cipher_text_final


def decode(password):
    cipher_suite = Fernet(b'nIoDjdsM388MiEbvlAo3LVpbPeLME5uDEovGH_kXKFg=')
    password=password.encode('UTF-8')
    plain_text = cipher_suite.decrypt(password).decode('UTF-8')
    plain_text_final = cipher_suite.decrypt(plain_text.encode('UTF-8')).decode('UTF-8')
    return plain_text_final


#------------------------------------------------------------------------------------------------------------


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
    if(allocated_fund):
        return allocated_fund[0]
    else:
        return 0

def get_POs(project_id):
    from models.PO import PO
    PO_list=PO.query.with_entities(PO.r_id,PO.quantity,PO.status).filter_by(project_id=project_id).all()
    return PO_list

#-------------------------------------------------------------------------------------------------------------------------

def get_members(username):
    from models.TEAM_MEMBERS import TEAM_MEMBERS;from models.TEAMS import TEAMS
    team = TEAMS.query.filter_by(team_leader=username).first()
    members=TEAM_MEMBERS.query.filter_by(team_id=team.team_id).all()
    return members


def get_leader_project_list(username):
    from models.TEAMS import TEAMS
    team = TEAMS.query.filter_by(team_leader=username).first()
    from models.PROJECTS import PROJECTS
    projects=PROJECTS.query.filter_by(team_id=team.team_id).all()
    for p in projects:
        p.set()
    return projects

#------------------------------------------------------------------------------------------

def get_del_edit_details(proj_id,del_id):
    return dbb.execute('SELECT del_name,del_desc,priority FROM \"DELIVERABLES\" where del_id=' + str(del_id) + 'and project_id=' + str(proj_id))

def get_project_edit_details(proj_id):
    return dbb.execute('SELECT project_name,project_desc,priority FROM \"PROJECTS\" where project_id=' + str(proj_id))