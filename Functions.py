from models.USERS import USERS
from cryptography.fernet import Fernet
import pandas as pd
import numpy as np
from app import dbb

def user_verification(p_username,p_password):
    print (p_username)
    user = USERS.query.filter_by(username=p_username).first()
    if user:
        print("Success")
        if decode(user.password) == p_password:
            print(user.role)
            return user
        else:
            print("Invalid Password")
            return False
    else:
        print("Wrong Username")
        return False

def encode(password):
    cipher_suite = Fernet(b'nIoDjdsM388MiEbvlAo3LVpbPeLME5uDEovGH_kXKFg=')
    cipher_text = cipher_suite.encrypt((password).encode('UTF-8'))
    cipher_text_final = cipher_suite.encrypt((cipher_text.decode('UTF-8')).encode('UTF-8'))
    cipher_text_final=cipher_text_final.decode('UTF-8')
    # print(cipher_text_final)
    return cipher_text_final


def decode(password):
    cipher_suite = Fernet(b'nIoDjdsM388MiEbvlAo3LVpbPeLME5uDEovGH_kXKFg=')
    password=password.encode('UTF-8')
    plain_text = cipher_suite.decrypt(password).decode('UTF-8')
    plain_text_final = cipher_suite.decrypt(plain_text.encode('UTF-8')).decode('UTF-8')
    return plain_text_final


#------------------------------------------------------------------------------------------------------------


def get_project_list(username):
    from models.PROJECTS import PROJECTS
    projects=PROJECTS.query.filter_by(username=username).all()
    for p in projects:
        p.set()
    return projects

def get_project(project_id):
    from models.PROJECTS import PROJECTS
    proj=PROJECTS.query.filter_by(project_id=project_id).first()
    proj.set()
    return proj


def get_del_list(project_id):
    from models.DELIVERABLES import DELIVERABLES
    deliverables=DELIVERABLES.query.filter_by(project_id=project_id).all()
    for d in deliverables:
        d.set()
    return deliverables

def get_del(del_id):
    from models.DELIVERABLES import DELIVERABLES
    deliverable=DELIVERABLES.query.filter_by(del_id=del_id).first()
    deliverable.set()
    return deliverable

def get_activities(del_id):
    from models.ACTIVITIES import ACTIVITIES
    activities=ACTIVITIES.query.filter_by(del_id=del_id).all()
    return activities


def predict(proj_details):
    data = pd.read_csv(r"C:\Users\Momin\Desktop\PROJECTS.xlsx")  # source file
    data.drop(data.columns[[0, 1, 2, 4, 5, 12, 14]], axis=1, inplace=True)
    data['phase'] = data['phase'].map({'Closure': 0, 'Initiation': 1, 'Planning': 2, 'Execution': 3})
    data['project_type'] = data['project_type'].map(
        {'Public Utilities': 0, 'Health Care': 1, 'Capital Goods': 2, 'Finance': 3, 'Consumer Services': 4,
         'Transportation': 5, 'Technology': 6, 'Miscellaneous': 7, 'Basic Industries': 8, 'Consumer Non-Durables': 9,
         'Consumer Durables': 10, 'Energy': 11, 'Other': 12, 'Development': 13})
    data['status'] = data['status'].map({'Completed': 0, 'In Process': 1})
    X = data.iloc[:, 0:7].values  # specify labels 0-7 prediction
    y = data.iloc[:, 7].values  # 8 to predict
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)
    from sklearn.ensemble import RandomForestRegressor

    regressor = RandomForestRegressor(n_estimators=250, random_state=0)
    regressor.fit(X_train, y_train)

    type_list={'Public Utilities': 0, 'Health Care': 1, 'Capital Goods': 2, 'Finance': 3, 'Consumer Services': 4,
         'Transportation': 5, 'Technology': 6, 'Miscellaneous': 7, 'Basic Industries': 8, 'Consumer Non-Durables': 9,
         'Consumer Durables': 10, 'Energy': 11, 'Other': 12, 'Development': 13}

    project_type = type_list[proj_details[2]]
    days_alloted = int(proj_details[3])
    status = 0
    phase = 0
    priority = int(proj_details[4])
    portfolio_id = 6
    team_id = int(proj_details[5])
    arr = [project_type, days_alloted, status, phase, priority, portfolio_id, team_id]

    test = np.asarray(arr)
    test = test.reshape(1, -1)
    y_pred = regressor.predict(test)
    print(y_pred)
    return int(y_pred);


def cust_pred():
    import pandas as pd
    import numpy as np
    import random
    import sklearn.linear_model
    data = pd.read_csv(r"C:\Users\Momin\Desktop\new_Customer.csv")  # source file
    data.drop(data.columns[[0, 4]], axis=1, inplace=True)
    data2 = data.groupby(['year', 'district'], as_index=False).count()
    data2.drop(['customer_name', 'country'], axis=1, inplace=True)
    ndistricts = np.unique(data2.district)
    data2 = pd.get_dummies(data=data2, columns=['district'])
    narray = np.asarray(data2)
    model = sklearn.linear_model.LinearRegression()
    X = narray[:, 2:len(ndistricts) + 2]
    y = narray[:, 1]
    model.fit(X, y)
    test = [1, 0, 0, 0, 0, 0,0]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test1 = test.reshape(1, -1)
    test1=model.predict(X=test1)
    # print(model.predict(X=test1))
    test = [0, 1, 0, 0, 0, 0,0]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test2 = test.reshape(1, -1)
    test2=model.predict(X=test2)
    # print(model.predict(X=test2))
    test = [0, 0, 1, 0, 0, 0,0]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test3 = test.reshape(1, -1)
    test3=model.predict(X=test3)
    # print(model.predict(X=test3))
    test = [0, 0, 0, 1, 0, 0,0]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test4 = test.reshape(1, -1)
    test4=model.predict(X=test4)
    # print(model.predict(X=test4))
    test = [0, 0, 0, 0, 1, 0,0]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test5 = test.reshape(1, -1)
    test5=model.predict(X=test5)
    # print(model.predict(X=test5))
    test = [0, 0, 0, 0, 0, 1,0]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test6 = test.reshape(1, -1)
    test6=model.predict(X=test6)
    # print(model.predict(X=test6))
    test = [0, 0, 0, 0, 0, 0,1]  # balochistan[1,0,0,0,0,0,0]#ajk[0,0,1,0,0,0,0]#fata[0,0,0,1,0,0,0]#islamabad[0,0,0,0,1,0,0]#kpk[0,0,0,0,0,1,0]#punjab[0,0,0,0,0,0,1]#sindh
    test = np.asarray(test)
    test7 = test.reshape(1, -1)
    test7=model.predict(X=test7)
    print(test7)

    cust_orders={'Balochistan':float(test1),'SINDH':float(test2),'AJK':float(test3),'FATA':float(test4),'ISLAMABAD':float(test5),'KPK':float(test6),'PUNJAB':float(test7)}
    print(cust_orders)
    l=[int(test1),int(test2),int(test3),int(test4),int(test5),int(test6),int(test7)]
    return l
    # return cust_orders

def get_allocated_fund(project_id):
    from models.FINANCES import FINANCES
    allocated_fund=FINANCES.query.with_entities(FINANCES.allocation).filter_by(project_id=project_id).first()
    if(allocated_fund):
        return allocated_fund[0]
    else:
        return 0

def get_POs(project_id):
    from models.PO import PO
    PO_list=PO.query.with_entities(PO.r_id,PO.quantity,PO.status).filter_by(project_id=project_id).all()
    return PO_list

#-------------------------------------------------------------------------------------------------------------------------

def get_members(username):
    from models.TEAM_MEMBERS import TEAM_MEMBERS;from models.TEAMS import TEAMS
    team = TEAMS.query.filter_by(team_leader=username).first()
    members=TEAM_MEMBERS.query.filter_by(team_id=team.team_id).all()
    return members


def get_leader_project_list(username):
    from models.TEAMS import TEAMS
    team = TEAMS.query.filter_by(team_leader=username).first()
    from models.PROJECTS import PROJECTS
    projects=PROJECTS.query.filter_by(team_id=team.team_id).all()
    for p in projects:
        p.set()
    return projects

#------------------------------------------------------------------------------------------

def get_del_edit_details(proj_id,del_id):
    return dbb.execute('SELECT del_name,del_desc,priority FROM \"DELIVERABLES\" where del_id=' + str(del_id) + 'and project_id=' + str(proj_id))

def get_project_edit_details(proj_id):
    return dbb.execute('SELECT project_name,project_desc,priority FROM \"PROJECTS\" where project_id=' + str(proj_id))

#portfolios
def get_portfolios():
    return dbb.execute('select pf.portfolio_name,p.project_name,SUM(p.quantity) as qty from \"PROJECTS\" as p,\"PORTFOLIO\" as pf where p.portfolio_id = pf.portfolio_id AND (CAST (end_date as text) BETWEEN \'2017-10%%\' AND \'2018-01%%\') GROUP BY pf.portfolio_name,p.project_name ORDER BY pf.portfolio_name')

#quantity of projs
def mps(start_date,end_date):
    return dbb.execute('SELECT pf.portfolio_name, p.project_name, p.start_date, p.end_date, p.quantity FROM \"PROJECTS\" as p,\"PORTFOLIO\" as pf  where (CAST(end_date as text) BETWEEN \'2017-10%%\' AND \'2018-01%%\') AND (p.portfolio_id = pf.portfolio_id) ORDER BY pf.portfolio_name')
