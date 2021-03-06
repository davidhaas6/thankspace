import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))

def load_json(filepath):
    return json.load(open(os.path.join(basedir, filepath)))

class Config(object):
    # SECRET_KEY = os.urandom(32)
    SECRET_KEY = 'static but secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Signals every time a change is made to the DB

    PLACEHOLDERS = load_json('resources/placeholders.json')['items']

    # Input
    MAX_HANDLE_LEN = 15
    MIN_HANDLE_LEN = 4
    HANDLE_REGEX = r'^\w+$'

    MAX_EMAIL_LEN = 120

    MAX_ITEM_LEN = 30

