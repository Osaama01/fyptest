from app import db
from models.USERS import USERS;from models.PROJECTS import PROJECTS
from models.DELIVERABLES import DELIVERABLES
from models.ACTIVITIES import ACTIVITIES

class COMMENTS(db.Model):
    __tablename__ = "COMMENTS"
    serial_num = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey(PROJECTS.project_id))
    del_id = db.Column(db.Integer, db.ForeignKey(DELIVERABLES.del_id))
    activity_id=db.Column(db.Integer, db.ForeignKey(ACTIVITIES.activity_id))
    username = db.Column(db.String(120), db.ForeignKey(USERS.username))
    comment=db.Column(db.String(4000))
    type=db.Column(db.String(120))

    def __init__(self,project_id=None, del_id=None,activity_id=None,username=None,comment=None,type=None):
        self.project_id = project_id
        self.del_id=del_id
        self.activity_id=activity_id
        self.username=username
        self.comment=comment
        self.type=type
