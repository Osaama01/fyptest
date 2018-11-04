from app import db

class DELIVERY_STORAGE(db.Model):
    __tablename__ = "DELIVERY_STORAGE"
    s_num = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('PROJECTS.project_id'))
    del_id = db.Column(db.Integer,db.ForeignKey('DELIVERABLES.del_id'))
    quantity = db.Column(db.Integer)

    def __init__(self, s_num=None, project_id=None, del_id=None, quantity=None):
        self.s_num = s_num
        self.project_id = project_id
        self.del_id=del_id
        self.quantity=quantity
