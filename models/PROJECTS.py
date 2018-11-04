from app import db

class PROJECTS(db.Model):
    __tablename__ = "PROJECTS"
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120))
    project_desc = db.Column(db.String(120))
    project_type = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    days_alloted = db.Column(db.Integer)
    status = db.Column(db.String(120))
    phase = db.Column(db.String(120))
    priority = db.Column(db.Integer)
    portfolio_id = db.Column(db.Integer,db.ForeignKey('PORTFOLIO.portfolio_id'))
    team_id = db.Column(db.Integer,db.ForeignKey('TEAMS.team_id'))
    po_pending = db.Column(db.Integer)
    issues = db.Column(db.Integer)
    username = db.Column(db.String(120),db.ForeignKey('USERS.username'))

    def __init__(self, project_id=None, project_name=None, project_desc=None, project_type=None, start_date=None, end_date=None, days_alloted=None, status=None, phase=None, priority=None, portfolio_id=None, team_id=None, po_pending=None, issues=None, username=None):
        self.project_id = project_id
        self.project_name = project_name
        self.project_desc = project_desc
        self.project_type = project_type
        self.start_date = start_date
        self.end_date = end_date
        self.days_alloted = days_alloted
        self.status = status
        self.phase = phase
        self.priority = priority
        self.portfolio_id = portfolio_id
        self.team_id = team_id
        self.po_pending = po_pending
        self.issues = issues
        self.username = username