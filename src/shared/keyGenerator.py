# -*- coding: utf-8 -*-
# Función para generar las keys de cada iteración, generadas por transposición.

# Genera la función de transposicion, segun la key ingresada.
# IN -> key: es la llave ingresada por el usuario.
# OUT -> swapKey: función de transposicion.
def keySeed(key):
	orderKey = sorted(key)
	swapKey = []

	for k in key:
		ind = orderKey.index(k)
		swapKey.append(ind)
		orderKey[ind] = None

	return swapKey


# Realiza la transposición de cada keyself.
# IN -> actKey: key actual a transponer.
# IN -> swapKey: función de transposición.
# OUT -> newKey: la nueva key despues de la transposición.
def swap(actKey, swapKey):
	newKey = ""
	for i in swapKey:
		newKey += actKey[i]

	return newKey


# Genera las llaves de cada iteración
# IN -> key: llave ingresada por el usuario
# IN -> it: cantidad de iteraciones, keys a generar.
# OUT -> keys: lista de keys.
def keyGenerator(key, it):
	keys = []
	swapKey = keySeed(key)
	# print(swapKey)

	for i in range(it):
		keys.append(key)
		key = swap(key, swapKey)

	return keys


# MAIN
# msg = "camilo"
# key = "camilo"
#
# keyGen = keyGenerator(key, 4)
# print(keyGen)
#
# # Ejemplo de como evaluar cada caso
# for i in range(1):
# 	for m, k in zip(msg, keyGen[i]):
# 		vm = ord(m) # Valor ASCII de la letre en el mensaje
# 		vk = ord(k) # Valor ASCII de la letre en la llave
# 		nv = (vm + vk) % 256
# 		nc = chr(nv) # Nuevo caracter ASCII, de reemplazo
# 		print('{0:1} {1:1} {2:3d} {3:3d} {4:3d} {5:1}'.format(m, k, vm, vk, nv, nc))
