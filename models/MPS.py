from app import db

class MPS(db.Model):
    __tablename__ = "MPS"
    mps_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('PROJECTS.project_id'))
    delivery_date = db.Column(db.Date)
    quantity = db.Column(db.Integer)

    def __init__(self, mps_id=None, project_id=None, delivery_date=None, quantity=None):
        self.mps_id = mps_id
        self.project_id = project_id
        self.delivery_date=delivery_date
        self.quantity=quantity
