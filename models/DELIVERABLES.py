from app import db
from Functions import get_activities

class DELIVERABLES(db.Model):
    __tablename__ = "DELIVERABLES"
    del_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('PROJECTS.project_id'))
    del_name = db.Column(db.String(120))
    del_desc = db.Column(db.String(120))
    priority = db.Column(db.Integer)
    Activities=None

    def __init__(self, del_id=None, project_id=None, del_name=None, del_desc=None, priority=None):
        self.del_id = del_id
        self.project_id = project_id
        self.del_name=del_name
        self.del_desc=del_desc
        self.priority=priority

    def set(self):
        self.Activities = get_activities(self.del_id)

