from flask import Flask, render_template,  request, redirect, url_for, session as flask_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from gevent.pywsgi import WSGIServer
from models import (
    Base, Department,
    Application, Client, User
)
from utils import login_required

engine = create_engine(
    'mysql+mysqlconnector://itea:itea@localhost/itea')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter(User.email == email,
                                          User.password == password).one_or_none()
        
        if user:
            flask_session['logged_in'] = user.email
            return redirect(url_for('departments'))
        return redirect(url_for('register'))
    return render_template('login.html')
   

@app.route('/departments', methods = ['GET', 'POST'])
@login_required
def departments():
    if request.method == 'POST':
        if not session.query(Department).filter(Department.city == request.form['city']).one_or_none():
            city = request.form['city']
            count_of_workers = request.form['count_of_workers']
            new_department = Department(city = city, count_of_workers = count_of_workers)
            session.add(new_department)
            session.commit()
        

    departments = session.query(Department).all()

    return render_template('tables.html', departments = departments)

@app.route('/applications', methods = ['GET', 'POST'], defaults = {'application_id': None})
@app.route('/applications/<int:application_id>', methods = ['GET', 'POST'])
@login_required
def applications(application_id):
    if application_id:
        application = session.query(Application).filter(Application.id == application_id).one_or_none()
        session.delete(application)
        session.commit()
        
    applications = session.query(Application).all()

    return render_template('applications.html', applications = applications)

@app.route('/departments/<int:department_id>', methods = ['GET', 'POST'])
def departments_detail(department_id = None):

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        education = request.form['education']
        passport = request.form['passport']
        city = request.form['city']
        age = request.form['age']
        new_client = Client(department_id = department_id, first_name = first_name, last_name = last_name, education = education, passport = passport, 
                                        city = city, age = age)
        session.add(new_client)
        session.commit()

    clients = session.query(Department).filter(Department.id == department_id).first().clients

    return render_template('departments_details.html', clients = clients)



@app.route('/departments/<int:department_id>/delete_client', methods = ['GET', 'POST'])
def delete_client(department_id = None):

    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        education = request.form['education']
        passport = request.form['passport']
        city = request.form['city']
        age = request.form['age']
        delete_client = Client(department_id = department_id, first_name = first_name, last_name = last_name, education = education, passport = passport, 
                                        city = city, age = age)
        
        session.delete(delete_client)
        session.commit()


    clients = session.query(Department).filter(Department.id == department_id).first().clients

    return render_template('delete_client.html', clients = clients)



@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        if not session.query(User).filter(User.email == request.form['email']).one_or_none():
            login = request.form['login']
            password = request.form['password']
            email = request.form['email']
            add_user = User(login = login, password = password, 
                                        email = email)
            session.add(add_user)
            session.commit()
            return redirect('/login')

        
    return render_template('register.html')



if __name__=='__main__':
    
    Base.metadata.create_all(engine)
    app.secret_key = b'secret key'
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()

    app.run(host='0.0.0.0', port=5000, debug = True)