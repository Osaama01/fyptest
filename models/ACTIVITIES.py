from app import db

class ACTIVITIES(db.Model):
    __tablename__ = "ACTIVITIES"
    activity_id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(120))
    project_id = db.Column(db.Integer, db.ForeignKey('PROJECTS.project_id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    days_alloted = db.Column(db.Integer)
    del_id = db.Column(db.Integer,db.ForeignKey('DELIVERABLES.del_id'))
    priority = db.Column(db.Integer)
    username = db.Column(db.String(120),db.ForeignKey('USERS.username'))
    status = db.Column(db.String(120))

    def __init__(self, activity_id=None, activity_name=None, project_id=None, start_date=None, end_date=None, days_alloted=None, del_id=None, priority=None, username=None, status=None):
        self.activity_id = activity_id
        self.activity_name = activity_name
        self.project_id=project_id
        self.start_date=start_date
        self.end_date=end_date
        self.days_alloted=days_alloted
        self.del_id = del_id
        self.priority = priority
        self.username = username
        self.status = status
