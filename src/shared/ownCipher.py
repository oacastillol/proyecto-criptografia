# -*- coding: utf-8 -*-
# Implementación de un algritmo de cifrado propio.

from keyGenerator import keyGenerator # Modulo encargado de generar las llaves, tomando comopartida la llave dada por el usuario.

# MAIN
msg = "camilo"
key = "camilo"

keyGen = keyGenerator(key, 4)
print(msg, key, keyGen)

# Ejemplo de como evaluar cada caso
for i in range(4):
	nMsg = ""
	for m, k in zip(msg, keyGen[i]):
		vm = ord(m) # Valor ASCII de la letre en el mensaje
		vk = ord(k) # Valor ASCII de la letre en la llave
		nv = (vm + vk) % 256
		nc = chr(nv) # Nuevo caracter ASCII, de reemplazo
		print('{0:1} {1:1} {2:3d} {3:3d} {4:3d} {5:1}'.format(m, k, vm, vk, nv, nc))
		nMsg += nc

	msg = nMsg
	print(nMsg)
