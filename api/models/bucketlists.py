from ..utils import db
from datetime import datetime


class Bucketlist(db.Model):
    __tablename__='bucketlists'
    bucket_id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.DateTime(),default=datetime.now())
    date_modified=db.Column(db.DateTime(),onupdate=datetime.now())
    #created_by=db.Column(db.Integer,db.ForeignKey('users.user_id',ondelete='CASCADE'))
    users=db.Column(db.Integer(),db.ForeignKey('users.user_id'))
    items=db.relationship('Item', backref='bucketlist', lazy=True)


    def __str__(self):
        return f"<Bucketlist {self.bucket_id}>"


    def save(self):
        db.session.add(self)
        db.session.commit() 




    def delete(self):
        db.session.delete(self)
        db.session.commit() 

