# import jwt
import os
import datetime
# from flask import json, Response, request, g
# from functools import wraps
# from ..models.UserModel import UserModel

import RSA

# class Auth():
#   """
#   Auth Class
#   """
#   @staticmethod
#   def generate_token(user_id):
#     """
#     Generate Token Method
#     """
#     try:
#       payload = {
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
#         'iat': datetime.datetime.utcnow(),
#         'sub': user_id
#       }
#       return jwt.encode(
#         payload,
#         os.getenv('JWT_SECRET_KEY'),
#         'HS256'
#       ).decode("utf-8")
#     except Exception as e:
#       return Response(
#         mimetype="application/json",
#         response=json.dumps({'error': 'error generando el token'}),
#         status=400
#       )
#
#   @staticmethod
#   def decode_token(token):
#     """
#     Decode token method
#     """
#     re = {'data': {}, 'error': {}}
#     try:
#       payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
#       re['data'] = {'user_id': payload['sub']}
#       return re
#     except jwt.ExpiredSignatureError as e1:
#       re['error'] = {'message': 'Su token expiro, por favor vuelva a logearse'}
#       return re
#     except jwt.InvalidTokenError:
#       re['error'] = {'message': 'Token invalido, por favor intentelo con un nuevo token'}
#       return re
#
#   @staticmethod
#   def auth_required(func):
#       """
#       Auth decorator
#       """
#       @wraps(func)
#       def decorated_auth(*args, **kwargs):
#           if 'api-token' not in request.headers:
#               return Response(
#                   mimetype="application/json",
#                   response=json.dumps({'error': 'El token de autenticación no está disponible, inicia sesión para obtener uno'}),
#                   status=400
#               )
#           token = request.headers.get('api-token')
#           data = Auth.decode_token(token)
#           if data['error']:
#               return Response(
#                   mimetype="application/json",
#                   response=json.dumps(data['error']),
#                   status=400
#               )
#           user_id = data['data']['user_id']
#           check_user = UserModel.get_one_user(user_id)
#           if not check_user:
#               return Response(
#                   mimetype="application/json",
#                   response=json.dumps({'error': 'el usuario no existe, token no válido'}),
#                   status=400
#               )
#           g.user = {'id': user_id}
#           return func(*args, **kwargs)
#       return decorated_auth



# FUNCIONES PROPIAS

# Función que genera el mensaje cifrado y firmado para la autenticación
# IN -> idUser, id del usuario
# IN -> publicKey, llave publica de la sesión del usuario
# IN -> privateKey, llave privada de la sesión del usuario
# OUT -> Mensaje cifrado
def generarAutenticacion(idUser, publicKey, privateKey):
	ini = datetime.datetime.utcnow()
	exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
	# print ('DATOS A USAR')
	# print ('publicKey:{0}, privateKey:{1}'.format(publicKey, privateKey))
	# print ('inicio dtime:{}'.format(ini))
	# print ('expira dtime:{}'.format(exp))
	# print ('usuario:{}'.format(idUser))

	tIni = datetimeToInt(ini)
	tExp = datetimeToInt(exp)
	dtimeIni = intToDatetime(tIni)
	dtimeExp = intToDatetime(tExp)
	# print ('inicio day:{0}, hour:{1}, moment:{2}'.format(tIni[0], tIni[1], tIni[2]))
	# print ('expira day:{0}, hour:{1}, moment:{2}'.format(tExp[0], tExp[1], tExp[2]))
	# print ('inicio dtime:{}'.format(dtimeIni))
	# print ('expira dtime:{}'.format(dtimeExp))

	# Cifrado y firmado
	# print ('\nCifrado y firma:')
	msg = tIni + tExp
	msg.append(idUser)
	# print ('       msg', msg)
	cifrado = RSA.encrypt(msg, publicKey)
	chash = hash(tIni, tExp, idUser)
	sign = RSA.digitalSignature(chash, privateKey)
	# print ('hash:{0}, sign:{1}'.format(h, sign))
	cifrado.append(sign)
	# print ('   cifrado', cifrado)

	return cifrado


# Función quye valida la autenticación
# IN -> cifrado, mensaje cifrado a evaluar, es una lista de enteros
# IN -> publicKey, llave publica de la sesión del usuario
# IN -> privateKey, llave privada de la sesión del usuario
# OUT -> idUser, id del usuario
# OUT -> dtIni, datetime con el inicio de sesión
# OUT -> dtExp, date time con la expiración de la sessión.
# OUT -> val, resultado de la verificación de la firma
def validarAutenticacion(cifrado, publicKey, privateKey):
	sign = cifrado.pop(7)

	# Prueba de descifrdo y verificación de firma
	# print ('\nDescifrado y validación de firma:')
	# print ('   cifrado', cifrado)
	mensaje = RSA.decrypt(cifrado, privateKey)
	# print ('descifrado', mensaje)

	tIni = mensaje[0:3]
	tExp = mensaje[3:6]
	idUser = mensaje[6]

	dtimeIni = intToDatetime(tIni)
	dtimeExp = intToDatetime(tExp)

	chash = hash(tIni, tExp, idUser)
	val = RSA.signatureVerification(chash, sign, publicKey)

	# print ('\nDatos recuperados:')
	# print ('usuario:{}'.format(idUser))
	# print ('inicio dtime:{}'.format(dtimeIni))
	# print ('expira dtime:{}'.format(dtimeExp))
	# print ('firma de verificación:', val)

	return idUser, dtimeIni, dtimeExp, val


# Función para pasar el datetime a formato numerico
# IN -> dtime
# OUT -> [day, hour, moment], día, hora y momento como enteros positivos
def datetimeToInt(dtime):
	time = str(dtime)
	day = int(time[0:4] + time[5:7] + time[8:10])
	hour = int(time[11:13] + time[14:16] + time[17:19])
	moment = int(time[20:])
	# print ('day:{0}, hour:{1}, moment:{2}'.format(day, hour, moment))
	return [day, hour, moment]


# Función para pasar conjunto de enteros a formato datatime
# IN -> timeInt tiempo como valores entero [day, hour, moment]
# OUT -> dtime, datatime de los valores ingresados
def intToDatetime(timeInt):
	day = str(timeInt[0]).zfill(8)
	hour = str(timeInt[1]).zfill(6)
	moment = str(timeInt[2]).zfill(6)
	dtime = datetime.datetime(int(day[0:4]), int(day[4:6]), int(day[6:8]), int(hour[0:2]), int(hour[2:4]), int(hour[4:]), int(moment))
	# print ('day:{0}, hour:{1}, moment:{2}'.format(day, hour, moment))
	# print ('dtime:{}'.format(dtime))
	return dtime


# Función que calcula un valor de verificación basado en datos de autenticaciónº
# IN -> tIni, valor entero relacionado con la fecha e inicio [day, hour, moment]
# IN -> tExp, valor entero relacionado con la fecha e expiración [day, hour, moment]
# IN -> Id del usuario
# OUT -> hash, valor calculado con los datos
def hash(tIni, tExp, idUser):
	fSum = (tIni[0] % idUser) + (tIni[1] % idUser) + (tIni[2] % idUser)
	lSum = (tExp[0] % idUser) + (tExp[1] % idUser) + (tExp[2] % idUser)
	hash = fSum * lSum
	# print ('fSum:{0}, lSum:{1}, hash:{2}'.format(fSum, lSum, hash))
	return hash


# MAIN
idUser = 23
publicKey, privateKey = RSA.MyOwnRSA()

print ('Usuario:{},\npublicKey:{},\nprivateKey:{}'.format(idUser, publicKey, privateKey))

cipher = generarAutenticacion(idUser, publicKey, privateKey)
print ('Mensaje cifrado', cipher)

idUser, tIni, tExp, val = validarAutenticacion(cipher, publicKey, privateKey)

if val:
	print ('Token valido')
	print ('Usuario:{},\nLogueo:{},\nSessión expira:{}'.format(idUser, tIni, tExp))
else:
	('EL TOKEN NO SE HA VALIDADO CORRECTAMENTE')
