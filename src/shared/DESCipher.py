import binascii
from keyGenDES import keyGenDES # Modulo encargado de generar las llaves, tomando como partida la llave dada por el usuario.

#tabla de permutacion para mensaje original
ip = [57, 49, 41, 33, 25, 17, 9,  1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6
	]

#tabla de expancion para manejo de parte derecha de mensaje y llave, inicio funcion f
expancion = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]

#Arreglo de tablas S para la funcion f, mitad funcion f
sbox = [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

#permutacion funal para 32 bits, final funcion f
p = [
		15, 6, 19, 20, 28, 11,
		27, 16, 0, 14, 22, 25,
		4, 17, 30, 9, 1, 7,
		23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10,
		3, 24
	]

#tabla de ip inversa, para paso final de DES
ipInv = [
		39,  7, 47, 15, 55, 23, 63, 31,
		38,  6, 46, 14, 54, 22, 62, 30,
		37,  5, 45, 13, 53, 21, 61, 29,
		36,  4, 44, 12, 52, 20, 60, 28,
		35,  3, 43, 11, 51, 19, 59, 27,
		34,  2, 42, 10, 50, 18, 58, 26,
		33,  1, 41,  9, 49, 17, 57, 25,
		32,  0, 40,  8, 48, 16, 56, 24
	]


#Genera el string de bits haciendo primero la conversion de string a hex y luego de hex a bits
#IN -> text: string a ser transformado
#IN -> encoding: Necesario para encode de string, encargado de reconocimiento de caracteres
#IN -> errors: Necesario para encode, define si muestra o no errores o adverencias, definido como no mostrar.
#OUT -> bitsres: resultado de correccion de bits con veros a la izquierda, para completar los 64bits
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    bitsres = bits.zfill(8 * ((len(bits) + 7) // 8))
    return bitsres


#Etapa final convertir a a caracter
def d_caracter (list1):

    lista = []
    for m in range(len(list1)):
        vm = str(chr(list1[m]))
        lista += [vm]
    #print (lista)
    return (lista)


#Realiza la permutacion del bloque entrante con la tabla correspondiente, usando un mapeo de funcion lambda
#IN -> tabla: tabla previamente generada que dará el orden resultante de la permutación
#IN -> bloque: el bloque de datos a modificar, en este caso el manejo de las llaves
#OUT-> lista de datos tratados para que el bloque quede organizado como la tabla dada
def permutar(tabla, bloque):
		return list(map(lambda x: bloque[x], tabla))


#Funcion de cifrado/desifrado, en ella se calculan las llaves a usar para la k y el mensaje resultante

def cipher(msg,key,type):

#tratado de la llave y posterior generacion de llaves
	keyB = text_to_bits(key)
	keyB = [keyB[i:i+1] for i in range(0, len(keyB), 1)]
	keyGen = keyGenDES(keyB)
#tratado del mensaje para algoritmo, resultado en bits de la primera permutacion IP
	mB = text_to_bits(msg)
	mB = [keyB[i:i+1] for i in range(0, len(mB), 1)]
	mB = permutar(ip, mB)


#division de mensaje luego de permutacion
	L = mB[:32]
	R = mB[32:]

	if type == "cipher":
		#iniciacion de iteracion para uso de llaves con su offsite cifrado
		it = 0
		itoff = 1
	else:
		#iniciacion de iteracion para uso de llaves con su offsite descifrado
		it = 15
		itoff = -1

	i = 0
	while i< 16:
		#temporal para ser reemplazado en proxima iteracion
		tempR = R[:]

		#permutacion de R con tabla expancion, inicio de funcion f
		R = permutar(expancion, R)

		#ejecucion de XOR (^) entre R y la llave. llenado de arreglo B inicial
		j = 0
		B = []
		while j < len(R):

			temp = ''.join(str(R[j]).strip("['']"))
			R[j] = int(temp) ^ int(keyGen[it][j])

			j += 1
			if j % 6 == 0:
				B.append(R[j-6:j])

		#iniciacion de arreglo Bn resultante, y posicion a comparar
		k = 0
		Bn = [0] * 32
		pos = 0
		while k < 8:
			#Suma de bits entre posiciones 1 y 6 de B[k]
			m = (B[k][0] << 1) + B[k][5]
			#Suma de posiciones 2,3,4 y 5 de B[k]
			n = (B[k][1] << 3) + (B[k][2] << 2) + (B[k][3] << 1) + B[k][4]

			#encontrar valor de las tablas SBOX[k]
			v = sbox[k][(m<<4) + n]

			#conversion del valor entero v a bits, primero mirando and con 1000 y luego corrimiento necesario
			Bn[pos] = (v & 8) >> 3
			Bn[pos + 1] = (v & 4) >> 2
			Bn[pos + 2] = (v & 2) >> 1
			Bn[pos + 3] = v & 1

			pos+=4
			k+=1

		#permutacion final de funcion f entre el Bn generado y la tabla p
		R = permutar(p,Bn)

		#Xor final del proceso, entre el nuevo R y el viejo L
		j=0
		while j < len(R):
			temp = ''.join(str(L[j]).strip("['']"))
			R[j] = R[j] ^ int(temp)
			j+=1

		#asignar nuevo L al viejo R guardado en temp
		L = tempR

		#se calcula siguiente paso a probar
		it += itoff

		i += 1

	#permutacion de ultimo paso entre bits completos y el ipInv
	fStep = permutar(ipInv, R + L)


	#Paso de bits a mensaje, primero pasandolo a Codigo ascii y finalmente a carcateres
	temp = ''.join(map(str,fStep))
	temp2 = '0b'
	bits = temp2 + temp
	#Paso a codigo ascii
	n = int(bits,2)
	hexar = binascii.unhexlify('%x' % n)
	#Paso a caracteres
	result = d_caracter(hexar)
	#print("final result", ''.join(map(str,result)))

	return result

#Funcion MAIN de algoritmo DES
#IN -> msg: mensaje completo en string a cifrar
#IN -> key: llave en string a ser usada
#IN -> type: tipo de cifrado, 'cipher' para cifrado, el resto es descifrado
def DES(msg,key,type):
	#verifica si la llave es de 8 caracteres
	if len(key)!=8:
		raise Exception("Llave de tamaño incorrecto")
		return -1

	#inicializacion de string respuesta y temporal para espacio de 8 caracteres por cifrado
	c = ""
	temp = ""

	#division del mensaje en espacios de 8 caracteres, guardado de respectivos cifrados
	while len(msg) > 7:
		temp = msg[:8]
		res = cipher(temp,key,type)
		c += ''.join(map(str,res))
		msg = msg[8:]
	#si el mensaje no es multiplo de 8 rellena con x al final y ejecuta ultima iteracion de msg para encontrar cifrado
	if len(msg) > 0:
		while len(msg) <8:
			msg = msg + 'x'
		res = cipher(msg,key,type)
		c += ''.join(map(str,res))
	#print("cipher", c)
	return c


# MAIN
#msg = "prueba01"
#key = "llave001"
#DES(msg,key,"cipher")
