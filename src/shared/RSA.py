# -*- coding: utf-8 -*-
# Función que implemeta el algoritmo RSA

import random
import math
from primeList import primeList # Lista de números primos a usar junto a MyOwnRSA
# primeList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
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
# IN -> m, mensaje a cifrar
# IN -> en, llave publica de cifrado
# OUT -> y, mensaje cifrado
def encrypt(m, en):
	c = []

	for i in m:
		z = powerMod(int(i), en[0], en[1])
		# print ('#:{0}, e:{1}, n:{2}, z:{3}'.format(int(i), en[0], en[1], z))
		c.append(z)

	return c


# Descifrado de mensaje
# IN -> c, mensaje a desifrar
# IN -> dn ,llave privada de descifrado
# OUT -> m, mensaje descifrado
def decrypt(c, dn):
	m = []

	for i in c:
		z = powerMod(int(i), dn[0], dn[1])
		# print ('#:{0}, d:{1}, n:{2}, z:{3}'.format(int(i), dn[0], dn[1], z))
		m.append(z)

	return m


# Algoritmo Euclidiano Extendido
# IN -> a, b enteros positivos donde: a>=b
# OUT -> d, x, y donde d = GCD(a,b) x, y enteros de modo que cumple ax + by = d
def extendedEuclideanAlgorithm (a, b):
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



# MAIN
# Prueba del algoritmo
# Publish, Keep = MyOwnRSA()
#
# print ("Public Key:", Publish)
# print ("Private Key: ", Keep)
#
# msg = "6882326879666683"
# m =[]
#
# step = math.ceil(len(msg)/num_bloq)
# for i in range(0, len(msg), step):
# 	val = msg[i:i+step]
# 	m.append(val)
#
# print ('msg', msg, m)
# c = encrypt(m, Publish)
# print ('encriptado', c)
# m = decrypt(c, Keep)
# print ('desencriptado', m)
