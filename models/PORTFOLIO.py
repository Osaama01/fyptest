from app import db

class PORTFOLIO(db.Model):
    __tablename__ = "PORTFOLIO"
    portfolio_id = db.Column(db.Integer, primary_key=True)
    portfolio_name = db.Column(db.Integer)
    username = db.Column(db.Integer,db.ForeignKey('USERS.username'))


    def __init__(self, portfolio_id=None,portfolio_name=None, username=None):
        self.portfolio_id = portfolio_id
        self.portfolio_name=portfolio_name
        self.username = username

