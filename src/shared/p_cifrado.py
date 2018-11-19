from .keyGenerator import keyGenerator # Modulo encargado de generar las llaves, tomando comopartida la llave dada por el usuario.
#NOTA: puede funcionar con 4 6 8 bytes o demas, tener cuidad con message y key
#El dogma del Algoritmo propio, asi igualmente se le llamara
def gimg1859():
    list1 = list('gimg1859')
    lista = []
    for m in range(len(list1)):
        vm = ord(list1[m])
        lista += [vm]
    print (lista)
    return lista
#Transforma en ascii el mensaje o la key y lo delvuelve como lista
def c_ascii (list1):
    #print(" c ascii : ", list1)
    lista = []
    for m in range(len(list1)):
        vm = ord(list1[m])
        lista += [vm]
    #print (lista)
    return lista

#Etapa final convertir a a caracter
def c_caracter (list1):

    lista = []
    for m in range(len(list1)):
        vm = str(chr(list1[m]))
        lista += [vm]
    #print (lista)
    return str(lista)

#suma byte por byte
#utilizado en la etapa inicial y final de nuestro Algoritmo
#utilizado en la 2 parte del bloque junto a la key generada
def c_suma (list1,list2):
    lista = []
    #lista1 = c_ascii (list1)
    #lista2 = c_ascii (list2)
    #print ("lista1: ",list1, " Lista2", list2)
    for m in range(len(list1)):
        lista.append((list1[m]+list2[m])%256)
        #print(list1,list2,lista,(len(list1)))
    return lista

# corrimiento a la izquierda
def c_corrimiento (list1):
    lista = []
    rango = int(len(list1))
    m=0
    #print(list1,rango,m)
    while m<(rango):
        if m<(rango-1):
            m += 1
            lista.append(list1[m])
            #print ('m: ', m , 'list : ',list)
        else:
            m += 1
            lista.append(list1[0])
            #print ('m: ', m , 'list : ',list)
    return lista
#Bloques, etapa intermedia, si es "l" o "r" --corta en la mitad y toma la primera o segunda parte
def c_bloque(list1,lr):
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
def c_unir (list1,list2):
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
#Rellena si es menor a 8 bytes con null en ASCII
def c_relleno(list1):
    #print(list1)
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

def pcifrado(lista_m, key):
    lista = []
        #Paso a cada letra y numero a ascii
    estatico = gimg1859()
    rango_m = len(lista_m)
    rango_k = len(key)
#     = c_ascii(message)
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
                list1.append(lista_m[m+rango])
            else:
                print ('error en rango de mensaje')
        #    print ('lis1: ',list1, 'lista_m: ',lista_m, "rango&m",(rango+m), 'rango: ',rango, 'm: ',m)
        #En dado caso que la key tenga mas de 8 bytes solo toma encuenta los primeros 8
        list2 = c_relleno(key)
        #Etapa inicial del Algoritmo gimg1859
        c_1 = c_suma(estatico,list1)
        #Estapa intermedia - podria usar un def mas pero mientras tanto asi
        l_0 = c_bloque(c_1,'l')
        r_0 = c_bloque(c_1,'r')

        l_1 = c_corrimiento(r_0)
        r_1 = c_suma(l_0,list2)

        l_2 = c_corrimiento(r_1)
        r_2 = c_suma(l_1, list2)

        l_3 = c_corrimiento(r_2)
        r_3 = c_suma(l_2, list2)

        l_4 = c_corrimiento(r_3)
        r_4 = c_suma(l_3, list2)

        #Etapa final de cifrado del Algoritmo gimg1859
        cunir = c_unir(l_4,r_4)
        c_2 = c_suma(estatico, cunir)
        #c = c_caracter(c_2)
        #c_2 muestra lo cifrado en ascii
        #print('cifrado gimg1859 en ascii: ',c_2)
        rango+=8
        lista+=c_2
        #print ('lista: ', lista, 'list1: ', list1, 'rango: ', rango, ' rango_m:',rango_m, (len(lista)))
    return lista #, rango_m
