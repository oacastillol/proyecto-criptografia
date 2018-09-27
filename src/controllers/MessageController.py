from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MessageModel import MessageModel, MessageSchema

message_api = Blueprint('message_api', __name__)
message_schema = MessageSchema()

@message_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Message Function
  """
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  data, error = message_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  message = MessageModel(data)
  message.save()
  data = message_schema.dump(message).data
  return custom_response(data, 201)

@message_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get All Messages
  """
  messages = MessageModel.get_all_messages_by_user(g.user.get('id'))
  data = message_schema.dump(messages, many=True).data
  return custom_response(data, 200)

@message_api.route('/<int:message_id>', methods=['GET'])
def get_one(message_id):
  """
  Get A Message
  """
  message = MessageModel.get_one_message(message_id)
  if not message:
    return custom_response({'error': 'mensaje no encontrado'}, 404)
  data = message_schema.dump(message).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permiso denegado'}, 400)
  return custom_response(data, 200)

@message_api.route('/<int:message_id>', methods=['PUT'])
@Auth.auth_required
def update(message_id):
  """
  Update A Message
  """
  req_data = request.get_json()
  message = MessageModel.get_one_message(message_id)
  if not message:
    return custom_response({'error': 'mensaje no encontrado'}, 404)
  data = message_schema.dump(message).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permiso denegado'}, 400)
  
  data, error = message_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  message.update(data)
  
  data = message_schema.dump(message).data
  return custom_response(data, 200)

@message_api.route('/<int:message_id>', methods=['DELETE'])
@Auth.auth_required
def delete(message_id):
  """
  Delete A Message
  """
  message = MessageModel.get_one_message(message_id)
  if not message:
    return custom_response({'error': 'mensaje no encontrado'}, 404)
  data = message_schema.dump(message).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permiso denegado'}, 400)
  message.delete()
  return custom_response({'message': 'eliminado'}, 204)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
)
