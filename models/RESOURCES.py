from app import db

class RESOURCES(db.Model):
    __tablename__ = "RESOURCES"
    r_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(120))
    resource_group = db.Column(db.String(120))
    quantity = db.Column(db.Integer)

    def __init__(self, r_id=None, resource_name=None, resource_group =None,quantity=None):
        self.r_id = r_id
        self.resource_name = resource_name
        self.resource_group = resource_group
        self.quantity=quantity