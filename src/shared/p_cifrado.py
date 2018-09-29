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
    return lista

# corrimiento a la izquierda
def c_corrimiento (list1):
    lista = []
    for m in range(len(list1)):
        #algo reacio con el modulo 256 pero dejarlo asi
        lista.append((list1[m-1])%256)
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
        #print('oo : ', lista)
    print (lista)
    return lista

def pcifrado(message, key):
    #print ('mensaje: ',message, " key ",key)
    #Paso a cada letra y numero a ascii
    estatico = gimg1859()
    list1 = c_ascii(message)
    list2 = c_ascii(key)
    #Etapa inicial del Algoritmo gimg1859
    #print ("Estatico : ", estatico, "list1 ",list1)
    c_1 = c_suma(estatico,list1)
    #Estapa intermedia - podria usar un def mas pero mientras tanto asi
    l_0 = c_bloque(c_1,l)
    r_0 = c_bloque(c_1,r)

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
    c = c_caracter(c_2)
    return (str(c))
#MAIN
#tupla inmutable [103, 105, 109, 103, 49, 56, 53, 57]
estatico = list('gimg1859')
message = list('sehizota')
key = list ('dddddddd')
r = 'r'
l = 'l'
#keyGen = keyGenerator(key, 5)
nzk = list(c_ascii(estatico))
#print (nzk)
#cbloque = c_bloque(nzk,l)
#cbloque1 = c_bloque(nzk,r)
#union = c_unir(cbloque,cbloque1)
#print ('bloque ',cbloque,cbloque1)
#print ('union ' ,union)
#print ('---------------')
#esta = gimg1859()
#print (" es gimg" ,esta)
ant = pcifrado(message,key)
print ('cifrado gimg1859: ' ,ant)
