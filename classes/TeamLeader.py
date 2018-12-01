from models.USERS import USERS;from models.COMMENTS import COMMENTS
from models.ACTIVITIES import ACTIVITIES
from models.DELIVERABLES import DELIVERABLES
from Functions import get_leader_project_list,get_members
from app import db
from app import dbb
import datetime


class TeamLeader(USERS):
    def __init__(self, username):
        super().__init__(username)
        self.projects=get_leader_project_list(username)
        self.members=get_members(username)


    def view_projects(self):
        print (self.projects)

    def get_projects(self):
        return self.projects

    def view_members(self):
        print(self.members)

    def get_members(self):
        return self.members

    def view_deliverable(self,project_id):
        for p in self.projects:
            if str(p.project_id) == str(project_id):
                print (p.deliverables)

    def get_deliverable(self,project_id):
        for p in self.projects:
            if str(p.project_id) == str(project_id):
                return (p.deliverables)

    def view_activities(self,project_id,del_id):
        for p in self.projects:
            if str(p.project_id) == str(project_id):
                for d in p.deliverables:
                    if str(d.del_id) == str(del_id):
                        print(d.Activities)

    def get_activities(self,project_id,del_id):
        for p in self.projects:
            if str(p.project_id) == str(project_id):
                for d in p.deliverables:
                    if str(d.del_id) == str(del_id):
                        return d.Activities

    def search_activity(self,project_id,del_id,activity_id):
            for p in self.projects:
                if str(p.project_id) == str(project_id):
                    for d in p.deliverables:
                        if str(d.del_id) == str(del_id):
                            for a in d.Activities:
                                if str(a.activity_id) == str(activity_id):
                                    return a.activity_id
            return False


    def add_comment(self,project_id,del_id,activity_id,p_comment):
        try:

            comment=COMMENTS(None,project_id,del_id,activity_id,None,p_comment)
            db.session.add(comment)
            db.session.commit()
            return True

        except:
            db.session.rollback()
            return False

    def add_comment(self,project_id,comment):
        try:

            comment=COMMENTS(project_id,None,None,None,comment)
            db.session.add(comment)
            db.session.commit()
            return True

        except:
            db.session.rollback()
            return False

    def report_issue(self, project_id,username,issue):
        try:

            comment=COMMENTS(project_id,None,None,username,issue,'issue')
            db.session.add(comment)
            db.session.commit()
            return True

        except:
            db.session.rollback()
            return False

    # def add_member(self,username):
        #One Member cannot be part of multiple teams


    def approve_activity(self,project_id,del_id,activity_id):
        try:
            dbb.execute(" UPDATE \"ACTIVITIES\" set status='Completed' where project_id="+str(project_id)+"and del_id="+str(del_id)+"and activity_id="+str(activity_id))
            now = datetime.datetime.now()
            dbb.execute(" UPDATE \"ACTIVITIES\" set end_date=\'"+now.strftime("%Y-%m-%d")+"\' where project_id="+str(project_id)+"and del_id="+str(del_id)+"and activity_id="+str(activity_id))
            return True

        except:
            print("Error")
            return False


    def assign_activity(self,activity_id,username):
        # try:
            dbb.execute(" UPDATE \"ACTIVITIES\" set username=\'"+username+"\' where activity_id="+str(activity_id)+"and username is null")
            now = datetime.datetime.now()
            dbb.execute(" UPDATE \"ACTIVITIES\" set start_date=\'"+now.strftime("%Y-%m-%d")+"\' where activity_id=" + str(activity_id))
            return True
        #
        # except:
        #     print("Error")
        #     return False


    def create_activity(self,project_id,del_id,details_list,username=None):
        try:
            result_set = dbb.execute("SELECT MAX(activity_id) FROM \"ACTIVITIES\"")  # Activity id for new project
            for r in result_set:
                activity_id = r[0] + 1
            if(username == None):
                activity=ACTIVITIES(activity_id,details_list[0],project_id,None,None,details_list[1],del_id,details_list[2],username,'In Process')
            else:
                now = datetime.datetime.now()
                activity = ACTIVITIES(activity_id, details_list[0], project_id,now.strftime("%Y-%m-%d"), None, details_list[1], del_id,details_list[2], username, 'In Process')
            db.session.add(activity)
            db.session.commit()
        except:
            db.session.rollback()
            return False



    def edit_deliverable(self,del_id,details_list): #Can change name, desc and priority
        dbb.execute(" UPDATE \"DELIVERABLES\" set del_name=\'"+details_list[0]+"\' ,del_desc=\'"+details_list[1]+"\' ,priority=\'"+str(details_list[2])+"\' where del_id="+str(del_id))
        return True



    def edit_activity(self,activity_id,details_list): #Can change name, desc and priority
        dbb.execute(" UPDATE \"ACTIVITIES\" set activity_name=\'"+details_list[0]+"\' ,priority=\'"+details_list[1]+"\' ,username=\'"+str(details_list[2])+"\' where activity_id="+str(activity_id))
        return True

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

    def mark_completed(self,project_id):
        try:
            dbb.execute(" UPDATE \"PROJECTS\" set phase='Closure' where project_id="+str(project_id))
            return True

        except:
            print("Error")
            return False


    def view_submitted_activities(self):
        submitted_activities=[]
        for p in self.projects:
                print(p)
                for d in p.deliverables:
                        for a in d.Activities:
                            if a.status == "In Process":
                                submitted_activities.append(a)
                            else:
                                continue
        return submitted_activities


    def view_completed_activities(self,project_id,del_id):
        completed_activities=[]
        for p in self.projects:
            if str(p.project_id) == str(project_id):
                for d in p.deliverables:
                    if str(d.del_id) == str(del_id):
                        for a in d.Activities:
                            if a.status == "Completed":
                                completed_activities.append(a)
                            else:
                                continue
        return len(completed_activities)

    def view_total_activities(self,project_id,del_id):
        sum=0
        for p in self.projects:
            if str(p.project_id) == str(project_id):
                for d in p.deliverables:
                    if str(d.del_id) == str(del_id):
                        return len(d.Activities)

    def view_completed_dels(self,project_id):
        completed_dels=[]
        for p in self.projects:
            if(str(p.project_id) == str(project_id)):
                for d in p.deliverables:
                    if(self.view_total_activities(project_id,d.del_id) == self.view_completed_activities(project_id,d.del_id)):
                        completed_dels.append(d)
        return completed_dels

    def view_incompleted_dels(self,project_id):
        incompleted_dels=[]
        for p in self.projects:
            if (str(p.project_id) == str(project_id)):
                for d in p.deliverables:
                    if(self.view_total_activities(project_id,d.del_id) != self.view_completed_activities(project_id,d.del_id)):
                        incompleted_dels.append(d)
        return incompleted_dels