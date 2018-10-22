import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Base, Department,
    Application, Client
)

engine = create_engine(
    'mysql+mysqlconnector://itea:itea@localhost/itea')
Session = sessionmaker(bind=engine)
session = Session()

def create_all_tables():
    Base.metadata.create_all(engine)

def upload_from_csv_and_add_to_db():
    with open('department.csv', 'r') as c_file:
        reader = csv.reader(c_file)
        for n, row in enumerate(reader):
            if n==0:
                pass
            else:
                department = Department(id=row[0],
                                        city=row[1],
                                        count_of_workers=row[2])
                session.add(department)

    with open('client.csv', 'r') as c_file:
        reader = csv.reader(c_file)
        for n, row in enumerate(reader):
            if n==0:
                pass
            else:
                client = Client(id=row[0],
                                first_name=row[1],
                                last_name=row[2],
                                education=row[3],
                                passport=row[4],
                                city=row[5],
                                age=row[6],
                                department_id=row[7])
                session.add(client)

    with open('application.csv', 'r') as c_file:
        reader = csv.reader(c_file)
        for n, row in enumerate(reader):
            if n==0:
                pass

            else:
                application = Application(
                    suma=row[1],
                    credit_state=row[2],
                    currency=row[3],
                    client_id=row[4])
                session.add(application)

    session.commit()

def custom_queries():
    res = session.query()
    print('1\n',)

if __name__=='__main__':
    create_all_tables()
    upload_from_csv_and_add_to_db()
    # custom_queries()