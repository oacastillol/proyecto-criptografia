from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .MessageModel import MessageSchema


class UserModel(db.Model):
    """
    User Model
    """
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    messages = db.relationship('MessageModel', backref='users', lazy=True) # add this new line
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        """
        Class constructor
        """
        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                item = self.__generate_hash(item) 
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)
    @staticmethod
    def get_user_by_username(value):
        return UserModel.query.filter_by(username=value).first()
  
    def __repr(self):
        return '<id {}>'.format(self.id)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    # add this new method
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)


class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  password = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  messages = fields.Nested(MessageSchema, many=True)
