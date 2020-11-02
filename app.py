from flask import Flask,request,render_template,flash,redirect,url_for,session,jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key='employee-project'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sa@123@localhost/employeedata'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    department = db.Column(db.String(50))
    contactno = db.Column(db.String(50))
    email = db.Column(db.String(50))
    birthdate = db.Column(db.DateTime)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))

    def __init__(self,fname,lname,dept,cno,email,bdate,uname,pwd):
        self.firstname = fname
        self.lastname = lname
        self.department = dept
        self.contactno = cno
        self.email = email
        self.birthdate = bdate
        self.username = uname
        self.password = pwd

@app.route('/')
def loginpage():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/emp-details')
def emp_details():
    if session.get('login') is None:
        return render_template('index.html')
    else:
        return render_template('employeedetails.html')

@app.route('/employee/create', methods=['POST'])
def employee_create():
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        department = request.form['department']
        contactno = request.form['contactno']
        email = request.form['email']
        idate = request.form['birthdate']
        username = request.form['username']
        password = request.form['password']

        emp = Employee(firstname,lastname,department,contactno,email,idate,username,password)
        db.session.add(emp)
        db.session.commit()

        flash("Data saved successfully","success")
        return redirect(url_for('loginpage'))

@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        empquery = Employee.query.filter_by(username=username,password=password).first()

        if empquery is not None:
            session['login'] = True
            session['firstname']=empquery.firstname
            session['lastname']=empquery.lastname
            session['department']=empquery.department
            session['contactno']=empquery.contactno
            session['email']=empquery.email
            session['birthdate']=empquery.birthdate
            return redirect(url_for('emp_details'))
        else:
            flash("Wrong credentials","warning")
            return redirect(url_for('loginpage'))

if __name__=='__main__':
    app.run(debug=True)