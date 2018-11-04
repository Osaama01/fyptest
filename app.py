from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://openpg:1234@localhost:5432/fyp'
db=SQLAlchemy(app)

@app.route('/divtest',methods=['GET', 'POST'])
def div_test():
    temp='<h1>Hello World</h1>'
    return render_template('asd.html',temp=temp)


@app.route('/Osama',methods=['GET', 'POST'])
def hello_Osama():
    return render_template('test.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['email'] != 'admin' or request.form['pass'] != 'admin':
            return 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('hello_Osama'))
    return render_template('Login.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
