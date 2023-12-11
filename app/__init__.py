import os
from flask import Flask

templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__,  template_folder=templates_path, static_url_path='', 
            static_folder=static_folder_path,)

from app import routes, utils

app.run(host="0.0.0.0", port=8080)