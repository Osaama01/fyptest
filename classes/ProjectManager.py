from models.USERS import USERS
from Functions import get_project_list

class ProjectManager(USERS):


    def __init__(self, username):
        super().__init__(username)
        self.projects=get_project_list(username)


    def view_projects(self):
        return self.projects
        