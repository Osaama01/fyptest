from app import db

class TEAMS(db.Model):
    __tablename__ = "TEAMS"
    team_id = db.Column(db.Integer, primary_key=True)
    team_leader = db.Column(db.String(120),db.ForeignKey('USERS.username'))

    def __init__(self, team_id=None,team_leader=None):
        self.team_id = team_id
        self.team_leader=team_leader
