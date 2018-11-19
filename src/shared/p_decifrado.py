from .keyGenerator import keyGenerator # Modulo encargado de generar las llaves, tomando comopartida la llave dada por el usuario.
#NOTA: puede funcionar con 4 6 8 bytes o demas, tener cuidad con message y key
#El dogma del Algoritmo propio, asi igualmente se le llamara
def gimg1859():
    list1 = list('gimg1859')
    lista = []
    for m in range(len(list1)):
        vm = ord(list1[m])
        lista += [vm]
    #print (lista)
    return lista
#Transforma en ascii el mensaje o la key y lo delvuelve como lista
def d_ascii (list1):
    lista = []
    rango = len(list1)
    for m in range(rango):
        vm = ord(list1[m])
        lista += [vm]
    #print (list1,lista, rango)
    return lista

#Etapa final convertir a a caracter
def d_caracter (list1):

    lista = []
    for m in range(len(list1)):
        vm = str(chr(list1[m]))
        lista += [vm]
    #print (lista)
    return (lista)

#suma byte por byte
#utilizado en la etapa inicial y final de nuestro Algoritmo
#utilizado en la 2 parte del bloque junto a la key generada
def d_resta(list1,list2):
    lista = []
    for m in range(len(list1)):
        lista.append(256-((list1[m]-list2[m])%256))
    return lista

def d_restainversa(list1,list2):
    lista = []
    for m in range(len(list1)):
        lista.append(((list1[m]-list2[m])%256))
    #print(lista,list1,list2)
    return lista
# corrimiento a la derecha
def d_corrimiento (list1):
    lista = []
    #print(list1)
    rango = len(list1)
    for m in range(rango):
        #Corrimiento a la derecha
        lista.append((list1[(m-1)]))
    #print(lista)
    return lista
#Bloques, etapa intermedia, si es "l" o "r" --corta en la mitad y toma la primera o segunda parte
def d_bloque(list1,lr):
    lista = []
    rango = int(len(list1)/2)
    #print ("List1 :",list1," lr: ",lr ," Rango: ", rango)
    if lr == 'l':
        for m in range(rango):
            lista.append(list1[m])
        return lista
            #break
    elif lr == 'r':
        for m in range(rango):
            lista.append(list1[m+(rango)])
        return lista
            #break
    else:
        print("Ome es 'l' o 'r' no otra vaina")
            #break
#Une los bloques l y r
def d_unir (list1,list2):
    lista = []
    rango = int(len(list1))
    for m in range(rango*2):
        if (m) < (rango):
            lista.append(list1[m])
        elif (m) >= (rango):
            lista.append(list2[m-rango])
        else:
            print("paso algo inesperado ome")
    return lista
def d_relleno(list1):
    lista = []
    rango = len(list1)
    if rango >8:
        for m in range (8):
            lista.append(list1[m])

    elif rango ==8:
        return list1
    elif rango < 8:
        for m in range (rango):
            lista.append(list1[m])
        for m in range (8-rango):
            if m ==1:
                m = rango
            lista.append(1)

    else:
        print ("tamano lista error menor que cero WDF!")
    #print ('relleno',lista)
    return lista
def p_mensaje(list1):
    atexto = ''.join(list1)
    return atexto
def pdecifrado(message, key):
    lista = []
        #Paso a cada letra y numero a ascii
    estatico = gimg1859()
    rango_m = len(message)
    c_rango=rango_m
    rango_k = len(key)
    rango  = 0
    while rango <= rango_m:
        #Arreglando bug del indexado
        if rango == rango_m:
            break
        list1 = []
        #envia a list1 lo comprendido de lista_m ASCII para esta iteracion

        for m in range (8):
            if (m+rango) >= rango_m:

                list1 = c_relleno(list1)
                m = 8
            elif rango <= rango_m:
                list1.append(message[m+rango])
            else:
                print ('error en rango de mensaje')

        #En dado caso que la key tenga mas de 8 bytes solo toma encuenta los primeros 8
        list2 = d_relleno(key)
        #[1, 253, 1, 253, 147, 158, 147, 158] mensaje cifrado
        #clave
        #Etapa inicial del Algoritmo gimg1859

        d_1 = d_resta(estatico,list1)
        #Estapa intermedia - podria usar un def mas pero mientras tanto asi
        l_0 = d_bloque(d_1,'l')
        r_0 = d_bloque(d_1,'r')

        r_1 = d_corrimiento(l_0)

        l_1 = d_restainversa(r_0,list2)

        l_2 = d_restainversa(r_1, list2)
        r_2 = d_corrimiento(l_1)

        l_3 = d_restainversa(r_2, list2)
        r_3 = d_corrimiento(l_2)

        l_4 = d_restainversa(r_3, list2)
        r_4 = d_corrimiento(l_3)

        #Etapa final de decifrado del Algoritmo gimg1859
        cunir = d_unir(l_4,r_4)
        d_2 = d_resta(estatico, cunir)
        #d = d_caracter(d_2)
        #lo muestra lo que vale en ascii
        #print ('decifrado en ascii',d_2)
        lista+=d_2
        rango+=8
        #Eliminar caracteres de relleno
        if rango>c_rango:
            eliminar = int(rango - c_rango)
            for k in range (eliminar):
                lista.pop()
    return (lista)

