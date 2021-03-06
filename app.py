# -------------------
# Imports
# -------------------

from flask import Flask, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
import json, os, requests
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import types
import flask.ext.restless


# -------------------
# Init
# -------------------

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)


# -------------------
# Settings
# -------------------

# THE_KEY = os.environ['FLASK_KEY']

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, PATCH, DELETE, OPTIONS'
    return response
app.after_request(add_cors_header)


# -------------------
# Models
# -------------------

class JsonType(Mutable, types.TypeDecorator):
    ''' JSON wrapper type for TEXT database storage.
    
        References:
        http://stackoverflow.com/questions/4038314/sqlalchemy-json-as-blob-text
        http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/mutable.html
    '''
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        return unicode(json.dumps(value))

    def process_result_value(self, value, engine):
        if value:
            return json.loads(value)
        else:
            # default can also be a list
            return {}

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode())
    code_url = db.Column(db.Unicode())
    link_url = db.Column(db.Unicode())
    description = db.Column(db.Unicode())
    type = db.Column(db.Unicode())
    categories = db.Column(db.Unicode())
    github_details = db.Column(JsonType())
    brigade = db.Column(db.Unicode)
    keep = db.Column(db.Boolean())
    
    def __init__(self, name, code_url=None, link_url=None,
                 description=None, type=None, categories=None, github_details=None, brigade=None, keep=None):
        self.name = name
        self.code_url = code_url
        self.link_url = link_url
        self.description = description
        self.type = type
        self.categories = categories
        self.github_details = github_details
        self.brigade = brigade
        self.keep = True


# -------------------
# API
# -------------------

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
exclude_columns = ['id','keep']
manager.create_api(Project, methods=['GET'], exclude_columns=exclude_columns, collection_name='projects', max_results_per_page=-1)


# -------------------
# Routes
# -------------------

@app.route("/")
def index():
    return '''<html>
<head>
    <title>Civic Tech Movement API</title>
</head>
<body>
    <p>Read more about me at <a href="https://github.com/codeforamerica/civic-json-worker#readme">codeforamerica/civic-json-worker</a>.</p>
    <p>Some data:</p>
    <ul>
    <li><a href="api/projects">Projects</a></li>
    </ul>
</body>
</html>'''

if __name__ == "__main__":
    app.run(debug=True)
