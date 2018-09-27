import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel


class Auth():
  """
  Auth Class
  """
  @staticmethod
  def generate_token(user_id):
    """
    Generate Token Method
    """
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error generando el token'}),
        status=400
      )

  @staticmethod
  def decode_token(token):
    """
    Decode token method
    """
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'user_id': payload['sub']}
      return re
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'Su token expiro, por favor vuelva a logearse'}
      return re
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Token invalido, por favor intentelo con un nuevo token'}
      return re
  
  @staticmethod
  def auth_required(func):
      """
      Auth decorator
      """
      @wraps(func)
      def decorated_auth(*args, **kwargs):
          if 'api-token' not in request.headers:
              return Response(
                  mimetype="application/json",
                  response=json.dumps({'error': 'El token de autenticación no está disponible, inicia sesión para obtener uno'}),
                  status=400
              )
          token = request.headers.get('api-token')
          data = Auth.decode_token(token)
          if data['error']:
              return Response(
                  mimetype="application/json",
                  response=json.dumps(data['error']),
                  status=400
              )
          user_id = data['data']['user_id']
          check_user = UserModel.get_one_user(user_id)
          if not check_user:
              return Response(
                  mimetype="application/json",
                  response=json.dumps({'error': 'el usuario no existe, token no válido'}),
                  status=400
              )
          g.user = {'id': user_id}
          return func(*args, **kwargs)
      return decorated_auth
