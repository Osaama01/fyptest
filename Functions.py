from models.USERS import USERS

def user_verification(p_username,p_password):
    print (p_username)
    user = USERS.query.filter_by(username=p_username).first()
    if user:
        print("Success")
        if user.password == p_password:
            print(user.role)
            return user
        else:
            print("Invalid Password")
            return False
    else:
        print("Wrong Username")
        return False

