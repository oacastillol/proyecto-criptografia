# import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel
from .RSA import encrypt, digitalSignature, decrypt, signatureVerification, public_key, private_key

class Auth():
#   """
#   Auth Class
#   """
	@staticmethod
	def generate_token(user_id):
#     """
#     Generate Token Method
#     """
		return Auth.generarAutenticacion(user_id,public_key, private_key)

	@staticmethod
	def decode_token(token):
#     """
#     Decode token method
#     """
		re = {'data': {}, 'error': {}}
		payload = Auth.validarAutenticacion(list(map(int,token.split(","))),public_key, private_key)
		if payload['sig']:
			actual = datetime.datetime.utcnow()
			if actual < payload['exp'] and actual > payload['ini']:
				re['data'] = {'user_id': payload['sub']}
				return re
			else:
				re['error'] = {'message': 'Su token expiro, por favor vuelva a logearse'}
				return re
		else:
			re['error'] = {'message': 'Token invalido, por favor intentelo con un nuevo token'}
			return re
		
	@staticmethod
	def auth_required(func):
#	"""
#	Auth decorator
#	"""
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
        
# FUNCIONES PROPIAS

# Función que genera el mensaje cifrado y firmado para la autenticación
# IN -> idUser, id del usuario
# IN -> publicKey, llave publica de la sesión del usuario
# IN -> privateKey, llave privada de la sesión del usuario
# OUT -> Mensaje cifrado
	@staticmethod
	def generarAutenticacion(idUser, publicKey, privateKey):
		ini = datetime.datetime.utcnow()
		exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
	# print ('DATOS A USAR')
		# print ('publicKey:{0}, privateKey:{1}'.format(publicKey, privateKey))
		# print ('inicio dtime:{}'.format(ini))
		# print ('expira dtime:{}'.format(exp))
		# print ('usuario:{}'.format(idUser))

		tIni = Auth.datetimeToInt(ini)
		tExp = Auth.datetimeToInt(exp)
		dtimeIni = Auth.intToDatetime(tIni)
		dtimeExp = Auth.intToDatetime(tExp)
		# print ('inicio day:{0}, hour:{1}, moment:{2}'.format(tIni[0], tIni[1], tIni[2]))
		# print ('expira day:{0}, hour:{1}, moment:{2}'.format(tExp[0], tExp[1], tExp[2]))
		# print ('inicio dtime:{}'.format(dtimeIni))
		# print ('expira dtime:{}'.format(dtimeExp))

		# Cifrado y firmado
		# print ('\nCifrado y firma:')
		msg = tIni + tExp
		msg.append(idUser)
		# print ('	 msg', msg)
		cifrado = encrypt(msg, publicKey)
		chash = Auth.hash(tIni, tExp, idUser)
		sign = digitalSignature(chash, privateKey)
		# print ('hash:{0}, sign:{1}'.format(h, sign))
		cifrado.append(sign)
		print ('   cifrado', cifrado)

		return cifrado


# Función quye valida la autenticación
# IN -> cifrado, mensaje cifrado a evaluar, es una lista de enteros
# IN -> publicKey, llave publica de la sesión del usuario
# IN -> privateKey, llave privada de la sesión del usuario
# OUT -> idUser, id del usuario
# OUT -> dtIni, datetime con el inicio de sesión
# OUT -> dtExp, date time con la expiración de la sessión.
# OUT -> val, resultado de la verificación de la firma
	@staticmethod
	def validarAutenticacion(cifrado, publicKey, privateKey):
		sign = cifrado.pop(7)

		# Prueba de descifrdo y verificación de firma
		# print ('\nDescifrado y validación de firma:')
		# print ('   cifrado', cifrado)
		mensaje = decrypt(cifrado, privateKey)
		# print ('descifrado', mensaje)

		tIni = mensaje[0:3]
		tExp = mensaje[3:6]
		idUser = mensaje[6]

		dtimeIni = Auth.intToDatetime(tIni)
		dtimeExp = Auth.intToDatetime(tExp)

		chash = Auth.hash(tIni, tExp, idUser)
		val = signatureVerification(chash, sign, publicKey)

		# print ('\nDatos recuperados:')
		# print ('usuario:{}'.format(idUser))
		# print ('inicio dtime:{}'.format(dtimeIni))
		# print ('expira dtime:{}'.format(dtimeExp))
		# print ('firma de verificación:', val)

		return {'sub':idUser, 'ini':dtimeIni, 'exp':dtimeExp, 'sig':val}


# Función para pasar el datetime a formato numerico
# IN -> dtime
# OUT -> [day, hour, moment], día, hora y momento como enteros positivos
	@staticmethod
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
	@staticmethod
	def intToDatetime(timeInt):
		day = str(timeInt[0]).zfill(8)
		hour = str(timeInt[1]).zfill(6)
		moment = str(timeInt[2]).zfill(6)
		print ('day:{0}, hour:{1}, moment:{2}'.format(day, hour, moment))
		dtime = datetime.datetime(int(day[0:4]), int(day[4:6]), int(day[6:8]), int(hour[0:2]), int(hour[2:4]), int(hour[4:]), int(moment))
		# print ('dtime:{}'.format(dtime))
		return dtime


# Función que calcula un valor de verificación basado en datos de autenticaciónº
# IN -> tIni, valor entero relacionado con la fecha e inicio [day, hour, moment]
# IN -> tExp, valor entero relacionado con la fecha e expiración [day, hour, moment]
# IN -> Id del usuario
# OUT -> hash, valor calculado con los datos
	@staticmethod
	def hash(tIni, tExp, idUser):
		fSum = (tIni[0] % idUser) + (tIni[1] % idUser) + (tIni[2] % idUser)
		lSum = (tExp[0] % idUser) + (tExp[1] % idUser) + (tExp[2] % idUser)
		hash = fSum * lSum
		# print ('fSum:{0}, lSum:{1}, hash:{2}'.format(fSum, lSum, hash))
		return hash


# MAIN
#idUser = 23
#publicKey, privateKey = RSA.MyOwnRSA()

#print ('Usuario:{},\npublicKey:{},\nprivateKey:{}'.format(idUser, publicKey, privateKey))

#cipher = generarAutenticacion(idUser, publicKey, privateKey)
#print ('Mensaje cifrado', cipher)

#idUser, tIni, tExp, val = validarAutenticacion(cipher, publicKey, privateKey)

#if val:
#	print ('Token valido')
#	print ('Usuario:{},\nLogueo:{},\nSessión expira:{}'.format(idUser, tIni, tExp))
#else:
#	('EL TOKEN NO SE HA VALIDADO CORRECTAMENTE')
