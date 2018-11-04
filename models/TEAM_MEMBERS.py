from app import db

class TEAM_MEMBERS(db.Model):
    __tablename__ = "TEAM_MEMBERS"
    index = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),db.ForeignKey('USERS.username'))
    team_id = db.Column(db.Integer,db.ForeignKey('TEAMS.team_id'))

    def __init__(self, index=None, username=None, team_id =None):
        self.index = index
        self.username = username
        self.team_id = team_id