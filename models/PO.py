from app import db
from models.PROJECTS import PROJECTS
from models.RESOURCES import RESOURCES

class PO(db.Model):
    __tablename__ = "PO"
    serial_num = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer,db.ForeignKey(PROJECTS.project_id))
    r_id = db.Column(db.Integer,db.ForeignKey(RESOURCES.r_id))
    quantity = db.Column(db.Integer)
    status=db.Column(db.CHAR(1))

    def __init__(self, serial_num=None,po_id=None, project_id=None, r_id=None,quantity=None,status=None):
        self.serial_num = serial_num
        self.po_id=po_id
        self.project_id = project_id
        self.r_id=r_id
        self.quantity=quantity
        self.status=status

    def view_details(self):
        print(self.project_id,self.r_id,self.quantity)
