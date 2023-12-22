import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__,  template_folder=templates_path, static_url_path='', 
            static_folder=static_folder_path,)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, utils

app.run(host="0.0.0.0", port=8080)