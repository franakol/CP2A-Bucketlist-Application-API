from ..utils import db
from datetime import datetime, date


class User(db.Model):
    __tablename__='users'
    user_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    username=db.Column(db.String(45),nullable=False,unique=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.Text(),nullable=False)
    date_created=db.Column(db.DateTime(),default=datetime.utcnow())
    date_modified=db.Column(db.DateTime(),onupdate=datetime.utcnow())
    bucketlists=db.relationship('Bucketlist',backref='', passive_deletes=True)
    
     
    def __init__(self, username, email, password, 
    date_created=None, date_modified=None):
        self.username = username
        self.email = email
        self.password = password
        if date_created is None:
            date_created = datetime.utcnow()
        else:
            date_created = datetime.strptime(date_created, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.date_created = date_created
        if date_modified is None:
            date_modified = datetime.utcnow()
        else:
            date_modified = datetime.strptime(date_modified, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.date_modified = date_modified


    def __repr__(self):
     return   f"<User {self.user_id} {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
        """saves user to the database"""

  # method for updating password
    def update_password(self, new_password):
        self.password = new_password
        db.session.commit()
        return "Password updated successfully"