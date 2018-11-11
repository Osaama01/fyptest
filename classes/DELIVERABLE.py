from models.DELIVERABLES import DELIVERABLES
from Functions import get_del,get_activities


class DELIVERABLE(DELIVERABLES):

    def __init__(self, del_id):
        deliverable=get_del(del_id)
        super().__init__(del_id, deliverable.project_id,deliverable.del_name,deliverable.del_desc,deliverable.priority)
        

    def view_projects(self):
        print(self.activities)
