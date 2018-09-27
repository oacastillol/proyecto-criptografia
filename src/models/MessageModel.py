from . import db
import datetime
from marshmallow import fields, Schema


class MessageModel(db.Model):
    """
    Message Model from users
    """
    __tablename__='messages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    cipher = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.title = data.get('title')
        self.cipher = data.get('cipher')
        self.owner_id = data.get('owner_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    @staticmethod
    def get_all_messages():
        return MessageModel.query.all()
  
    @staticmethod
    def get_one_message(id):
        return MessageModel.query.get(id)
    @staticmethod
    def get_all_messages_by_user(value):
        return MessageModel.query.filter_by(owner_id=value).all()
    
    def __repr__(self):
        return '<id {}>'.format(self.id)


class MessageSchema(Schema):
  """
  Message Schema
  """
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  cipher = fields.Str(required=True)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
