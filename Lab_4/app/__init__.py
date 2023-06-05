from flask import Flask
from flask_sqlalchemy import SQLAlchemy


host = "db"
database = "db_labs"
user = "postgres"
password = "23102002Papa"
port = "5432"

db = SQLAlchemy()

def app_obj():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    db.init_app(app)

    # this is needed in order for database session calls (e.g. db.session.commit)
    with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
      finally:
          print(
              "db.create_all() in __init__.py was successfull - no exceptions were raised")

    return app