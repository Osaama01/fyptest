from models.USERS import USERS;from models.COMMENTS import COMMENTS
from models.PROJECTS import PROJECTS;from models.DELIVERABLES import DELIVERABLES
from models.RESOURCES import RESOURCES
from models.PO import PO
from Functions import get_project_list
from app import db
from app import dbb

class ProjectManager(USERS):

    def __init__(self, username):
        super().__init__(username)
        self.projects=get_project_list(username)


    def view_projects(self):
        print (self.projects)
        return

    def view_deliverable(self,project_id):
        for p in self.projects:
            if p.project_id == project_id:
                print (p.deliverables)

    def search_project(self,project_id):
        for p in self.projects:
            if p.project_id == project_id:
                return p
        return False

    def get_projects(self):
        return self.projects

    def create_project(self,details_list):
        try:
            result_set = dbb.execute("SELECT MAX(project_id) FROM \"PROJECTS\"")  # Project id for new project
            for r in result_set:
                project_id = r[0] + 1
            new_proj = PROJECTS(project_id, details_list[0], details_list[1], details_list[2], None, None,
                                details_list[3], "In Process", "Initiation", details_list[4], 1, details_list[5], 0, 0,
                                details_list[6])
            db.session.add(new_proj)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def view_submitted_projects(self):
        submitted_projects=[]
        for p in self.projects:
            if p.status == "Submitted":
                submitted_projects.append(p)
            else:
                continue
        return submitted_projects

    def close_project(self,project_id):
        try:
            dbb.execute(" UPDATE \"PROJECTS\" set status='Completed' where project_id="+str(project_id))
            return True

        except:
            print("Error")
            return False

    def add_comment(self,project_id,comment):
        try:

            comment=COMMENTS(None,project_id,None,None,None,comment)
            db.session.add(comment)
            db.session.commit()
            return True

        except:
            db.session.rollback()
            return False

    def create_deliverable(self,project_id, details_list):

        try:
            result_set = dbb.execute("SELECT MAX(del_id) FROM \"DELIVERABLES\"")  # Deliverable id for new project
            for r in result_set:
                del_id = r[0] + 1
            new_del = DELIVERABLES(del_id,project_id , details_list[0], details_list[1],details_list[2])
            db.session.add(new_del)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


    def edit_deliverable(self,del_id,details_list): #Can change name, desc and priority
        dbb.execute(" UPDATE \"DELIVERABLES\" set del_name=\'"+details_list[0]+"\' ,del_desc=\'"+details_list[1]+"\' ,priority=\'"+str(details_list[2])+"\' where del_id="+str(del_id))
        return True


    def edit_project(self, project_id, details_list): #Can change name, desc and priority
        dbb.execute(" UPDATE \"PROJECTS\" set project_name=\'" + details_list[0] + "\' ,proj_desc=\'" + details_list[1] + "\' ,priority=\'" + str(details_list[2]) + "\' where project_id=" + str(project_id))
        return True

    def request_PO(self,project_id,list):
        try:
            result_set = dbb.execute("SELECT MAX(serial_num) FROM \"PO\"")  # Serial id for new project
            for r in result_set:
                serial_num = r[0] + 1
            result_set = dbb.execute("SELECT MAX(po_id) FROM \"PO\"")  # Purchase order id for new project
            for r in result_set:
                po_id = r[0] + 1
            for orders in list:
                resource = RESOURCES.query.with_entities(RESOURCES.r_id).filter_by(resource_name=orders[0]).first()
                po=PO(serial_num,po_id,project_id,resource[0],orders[1],'N')
                db.session.add(po)
                db.session.commit()
                serial_num+=1
            return True
        except:
            db.session.rollback()
            return False
