#Permutacion y reduccion PC1
pc1 = [56, 48, 40, 32, 24, 16,  8,
		  0, 57, 49, 41, 33, 25, 17,
		  9,  1, 58, 50, 42, 34, 26,
		 18, 10,  2, 59, 51, 43, 35,
		 62, 54, 46, 38, 30, 22, 14,
		  6, 61, 53, 45, 37, 29, 21,
		 13,  5, 60, 52, 44, 36, 28,
		 20, 12,  4, 27, 19, 11,  3
    ]

#Permutacion y reduccion PC2
pc2 = [
		13, 16, 10, 23,  0,  4,
		 2, 27, 14,  5, 20,  9,
		22, 18, 11,  3, 25,  7,
		15,  6, 26, 19, 12,  1,
		40, 51, 30, 36, 46, 54,
		29, 39, 50, 44, 32, 47,
		43, 48, 38, 55, 33, 52,
		45, 41, 49, 35, 28, 31
	]

#Rotaciones para los 16 casos de llaves
left_rotations = [
		1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
	]

#Realiza la permutacion del bloque entrante con la tabla correspondiente, usando un mapeo de funcion lambda
#IN -> tabla: tabla previamente generada que dará el orden resultante de la permutación
#IN -> bloque: el bloque de datos a modificar, en este caso el manejo de las llaves
#OUT-> lista de datos tratados para que el bloque quede organizado como la tabla dada
def permutar(tabla, bloque):
		return list(map(lambda x: bloque[x], tabla))

# Genera las llaves de cada iteración
# IN -> key: llave ingresada por el usuario STRING
# OUT -> keys: lista de keys.
def keyGenDES(key):

    #Primera permutacion pc1 para las llaves
    keyB = permutar(pc1, key)

    keys = [[0] * 48] * 16
    C = []
    D = []
    i = 0

    #Dividir el k en derecha e izquierda
    C = keyB[:28]
    D = keyB[28:]
    while i < 16:
        j = 0

        #Realizar corrimiento en divididos
        while j < left_rotations[i]:
            C.append(C[0])
            del C[0]

            D.append(D[0])
            del D[0]

            j += 1
        #permutacion de pc2 y guardado de cada llave resultante
        keys[i] = permutar(pc2, C + D)
        keys[i][0] = keys[i][0].split()
        i += 1
    print("C",type(C))
    print("D",type(D))
    print("K",type(keys[0][0]))
    return keys

#key = 'okijuhyg'
#keyGenDES(key)
