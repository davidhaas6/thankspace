from datetime import datetime
from app import db, login

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User @{self.handle}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item1 = db.Column(db.String(50))
    item2 = db.Column(db.String(50))
    item3 = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
print("here2")


def create_user(handle: str, email: str, password: str):
    u = User(handle=handle, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u


def create_post(user: User, items: list):
    if len(items) != 3:
        raise ValueError("Items must have exactly three elements")

    p = Post(item1=items[0], item2=items[1], item3=items[2], author=user)
    db.session.add(p)
    db.session.commit()
    
    return p


