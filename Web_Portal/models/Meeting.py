from ..mixins import MeetingMixin
from .. import db

class Meeting(MeetingMixin, db.Model):
    """description of class"""
    __bind_key__ = "meetings"
    __tablename__ = 'meetings'
    db = db
    failed = False
    reason_fail = ""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,  nullable=False)
    title = db.Column(db.String(120),  nullable=False)
    description = db.Column(db.String(120))
    dir = db.Column(db.String(120),  nullable=False)
    video = db.Column(db.String(120))
    documents = db.Column(db.PickleType)

    def __init__(self, *args, **kwargs):
        return super().__init__(db, *args, **kwargs)
