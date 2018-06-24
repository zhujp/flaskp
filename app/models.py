from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False,default='')
    email = db.Column(db.String(40), unique=True, nullable=False,default='')
    mobile = db.Column(db.String(20), unique=True,nullable=False,default='')
    password_hash = db.Column(db.String(255),nullable=False,default='')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True,nullable=False,default='')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.name

    users = db.relationship('User',backref='role')