from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def create():
    """
  Create User Function
  """
    req_data = request.get_json()
    data, error = user_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    if not data.get('username') or not data.get('password'):
        return custom_response({
            'error':
            'Necesitas un usuario y una contraseña para registrarte'
        }, 400)
    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_username(data.get('username'))
    if user_in_db:
        message = {
            'error':
            'El usuario ya existe, por favor seleccione otro nombre de usuario'
        }
        return custom_response(message, 400)
    user = UserModel(data)
    user.save()
    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'jwt_token': token}, 201)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True).data
    return custom_response(ser_users, 200)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    if not data.get('username') or not data.get('password'):
        return custom_response({
            'error':
            'Necesitas un usuario y una contraseña para iniciar sesión'
        }, 400)
    user = UserModel.get_user_by_username(data.get('username'))
    if not user:
        return custom_response({'error': 'credenciales no validas'}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'credenciales no validas'}, 400)
    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'jwt_token': token}, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
  Get a single user
  """
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'no se encuentra el usuario'}, 404)

    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
  Update me
  """
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
  Delete a user
  """
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'Eliminado'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
  Get me
  """
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


def custom_response(res, status_code):
    """
  Custom Response Function
  """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code)
