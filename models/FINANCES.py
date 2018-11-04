from app import db

class FINANCES(db.Model):
    __tablename__ = "FINANCES"
    finance_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('PROJECTS.project_id'))
    allocation = db.Column(db.Integer)
    release = db.Column(db.Integer)
    balance = db.Column(db.Integer)

    def __init__(self, finance_id=None, project_id=None, allocation=None, release=None,balance=None):
        self.finance_id = finance_id
        self.project_id = project_id
        self.allocation=allocation
        self.release=release
        self.balance = balance
