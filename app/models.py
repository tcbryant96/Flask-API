from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship("Post", backref= "author", lazy= 'dynamic')
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Save the password as the hashed version of the password
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def set_password(self,password):
        self.password = generate_password_hash(password)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "date_created": self.date_created,
            "password": self.password
        }
    

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable =False)
    body = db.Column(db.String(225), nullable=False)
    data_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()   

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in ('title', 'body'):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "date_created": self.data_created,
            "user_id": self.user_id
        }
    