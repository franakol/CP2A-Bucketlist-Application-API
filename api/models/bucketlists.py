from ..utils import db
from datetime import datetime


class Bucketlist(db.Model):
    __tablename__='bucketlists'
    bucket_id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.DateTime(),default=datetime.now())
    date_modified=db.Column(db.DateTime(),onupdate=datetime.now())
    created_by=db.Column(db.Integer,db.ForeignKey('users.user_id',ondelete='CASCADE'))
    items=db.relationship('Item', backref='bucketlist', passive_deletes=True)


    def __init__(self, name, date_created, created_by):
        """Initialize the bucketlist with a name and its creator."""
        self.name = name
        self.date_created = date_created
        self.created_by = created_by


    def __str__(self):
        return f"<Bucketlist {self.bucket_id}>"


    def save(self):
        db.session.add(self)
        db.session.commit() 




    def delete(self):
        db.session.delete(self)
        db.session.commit() 

    # @classmethod
    # def get_by_id(cls,id):
    #     return cls.query.get_or_404(id)



