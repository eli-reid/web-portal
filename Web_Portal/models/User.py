from ..mixins import UserMixin
from .. import db as db

class User(UserMixin, db.Model):

    __bind_key__ = "auth"
    __tablename__ = 'users'
    db = db
    failed = False
    reason_fail = ""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    change_pw = db.Column(db.Boolean, default=False, nullable=False)
    profile = db.relationship('Profile', backref='users', uselist=False)
    verification_key = db.Column(db.String(120), nullable=True)
    admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
