from .. import db

class Profile(db.Model):
    """description of class"""
    __bind_key__ = "auth"
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120),  nullable=False)
    last_name = db.Column(db.String(120),  nullable=False)
    address1 = db.Column(db.String(120),  nullable=False)
    address2 = db.Column(db.String(120),  nullable=True)
    city = db.Column(db.String(120),  nullable=False)
    state = db.Column(db.String(4),  nullable=False)
    zip = db.Column(db.String(30),  nullable=False)
    home_phone = db.Column(db.String(30),  nullable=True)
    mobile_phone = db.Column(db.String(30),  nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

