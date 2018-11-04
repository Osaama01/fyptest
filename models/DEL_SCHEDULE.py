from app import db

class DEL_SCHEDULE(db.Model):
    __tablename__ = "DEL_SCHEDULE"
    project_id = db.Column(db.Integer,db.ForeignKey('PROJECTS.project_id'))
    delivery_date = db.Column(db.Date)
    del_id = db.Column(db.Integer,db.ForeignKey('DELIVERABLES.del_id'))
    quantity = db.Column(db.Integer)
    serial_num = db.Column(db.Integer, primary_key=True)

    def __init__(self, serial_num=None, delivery_date=None, project_id=None, del_id=None, quantity=None):
        self.serial_num = serial_num
        self.project_id = project_id
        self.del_id=del_id
        self.quantity=quantity
        self.delivery_date=delivery_date
