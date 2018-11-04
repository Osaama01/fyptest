from app import db

class USERS(db.Model):
    __tablename__ = "USERS"
    username = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    dob = db.Column(db.String(120))
    role = db.Column(db.String(120))

    def __init__(self, username=None, password=None, firstname=None, lastname=None, dob=None, role=None):
        self.username = username
        self.password = password
        self.first_name=firstname
        self.last_name=lastname
        self.dob=dob
        self.role=role