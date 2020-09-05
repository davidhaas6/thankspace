from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Bootstrap
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

# DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User authentication
from flask_login import LoginManager
login = LoginManager(app)




from app import routes, models