from ..utils import db
from datetime import datetime


class User(db.Model):
    __tablename__='users'
    user_id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(45),nullable=False,unique=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    password_harsh=db.Column(db.Text(),nullable=False)
    date_created=db.Column(db.DateTime(),default=datetime.now())
    date_modified=db.Column(db.DateTime(),onupdate=datetime.now())
    bucketlists=db.relationship('Bucketlist',backref="",lazy=True)
    

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
        """saves user to the database"""