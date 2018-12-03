# -*- coding: utf-8 -*-
# Función que implemeta el algoritmo RSA

import random
import math
from .primeList import primeList # Lista de números primos a usar junto a MyOwnRSA

num_bloq = 6


# Implemetación propia del algoritmo RSA
# IN -> nada
# OUT -> (e,n), (d,n) par de claves Píblica y Privada
def MyOwnRSA():
	sr = random.SystemRandom()
	# p = sr.choice(primeList)
	# q = sr.choice(primeList)
	p, q = random.sample(primeList, 2)
	# p, q = 47,71
	n = p*q
	phi = (p-1)*(q-1)

	# al seleccionar e como otro primo de la lista se cumple MCD(phi,e) = 1
	e = sr.choice(primeList)
	# e = 79
	while e >= phi or e == p or e == q:
		e = sr.choice(primeList)

	EEA = extendedEuclideanAlgorithm(phi,e)
	d = EEA[2] if (EEA[2]>0) else phi+EEA[2]
	# print ('p:{0}, q:{1}, n:{2}, phi:{3}, e:{4}, d:{5}, EEA:{6}'.format(p, q, n, phi, e, d, EEA))
	return (e,n), (d,n)


# Cifrado de mensaje
# IN -> m, mensaje a cifrar (conjunto valores enteros positivos)
# IN -> en, llave publica de cifrado
# OUT -> y, mensaje cifrado
def encrypt(m, en):
	c = []

	for i in m:
		z = powerMod(i, en[0], en[1])
		# print ('#:{0}, e:{1}, n:{2}, z:{3}'.format(i, en[0], en[1], z))
		c.append(z)

	return c


# Descifrado de mensaje
# IN -> c, mensaje a desifrar (conjunto valores enteros positivos)
# IN -> dn , llave privada de descifrado
# OUT -> m, mensaje descifrado
def decrypt(c, dn):
	m = []

	for i in c:
		z = powerMod(i, dn[0], dn[1])
		# print ('#:{0}, d:{1}, n:{2}, z:{3}'.format(i, dn[0], dn[1], z))
		m.append(z)

	return m


# Firma Digital
# IN -> m, mensaje a cifrar (conjunto valores enteros positivos)
# IN -> en, llave privada de cifrado
# OUT -> y, mensaje cifrado
def digitalSignature(hash, dn):
	y = powerMod(hash, dn[0], dn[1])
	# print ('hash:{0}, d:{1}, n:{2}, y:{3}'.format(hash, dn[0], dn[1], y))
	return y


# Validación de firma
# IN -> x, y, valores para validación firma y firma cifrada
# IN -> en, llave publica de descifrado
# OUT -> True/False, resultado de la validación de la firma
def signatureVerification(hash, y, en):
	v = powerMod(y, en[0], en[1])
	# print ('hash:{0}, y:{1}, e:{2}, n:{3}, v:{4}'.format(hash, y, en[0], en[1], v))
	return True if v == hash else False


# Algoritmo Euclidiano Extendido
# IN -> a, b enteros positivos donde: a>=b
# OUT -> d, x, y donde d = GCD(a,b) x, y enteros de modo que cumple ax + by = d
def extendedEuclideanAlgorithm(a, b):
	if b == 0:
		# print (a, b, '-', a, 1, 0)
		return a, 1, 0

	q = a//b
	dp, xp, yp = extendedEuclideanAlgorithm(b, a % b)
	d, x, y = dp, yp, xp - q * yp

	# if y < 0:
	# 	y = y + a

	# print ('a:{0}, b:{1}, q:{2}, d:{3}, x:{4}, y:{5}'.format(a, b, q, d, x, y))
	return d, x, y


# Exponenciación Modular
# IN -> a, b, n valores enteros
# OUT -> z, donde z = a^b mod n
def powerMod(a, b, n):
	bin = []
	z = 1

	while b > 0: # Pasa número a binario
		bin.append(b % 2)
		b = b//2

	bin.reverse()

	for i in bin:
		if i == 1:
			z = (z**2 * a) % n
		else:
			z = z**2 % n

	# print ('bin:{0}\nz:{1}'.format(bin, z))
	return z


public_key, private_key = MyOwnRSA()
# MAIN
# Prueba del algoritmo
# generación de llaves
# Publish, Keep = MyOwnRSA()
# print ("Public Key:", Publish)
# print ("Private Key: ", Keep)
#
# # Creación de mensaje de prueba en bloques tratables
# msg = '6882326879666683'
# m = []
# step = math.ceil(len(msg)/num_bloq)
# for i in range(0, len(msg), step):
# 	val = msg[i:i+step]
# 	m.append(int(val))
# print ('msg', msg, m)
#
# # Pruebas de cifrado y descifrado se maneja una lista de valores para ello
# c = encrypt(m, Publish)
# print ('cifrado', c)
# m = decrypt(c, Keep)
# print ('descifrado', m)
#
# # Pruebas de firma digital, un solo valor para firmar o validar
# hash = 123
# print ('hash: ', hash)
# ds = digitalSignature(hash, Keep)
# print ('firma digital: ', ds)
# dv = signatureVerification(hash, ds, Publish)
# print ('validación firma: ', dv)
