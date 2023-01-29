from ..utils import db
from datetime import datetime


class Item(db.Model):
    __tablename__='items'
    item_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text, nullable=False)
    date_created=db.Column(db.DateTime(),default=datetime.now())
    date_modified = db.Column(db.DateTime(),onupdate=datetime.now())
    # done = db.Column(db.Boolean, default=False)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlists.bucket_id',ondelete='CASCADE'))


    def __repr__(self):
        return f"<Item {self.item_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit() 




    def delete(self):
        db.session.delete(self)
        db.session.commit() 

    # @classmethod
    # def get_by_id(cls,id):
    #     return cls.query.get_or_404(id)


