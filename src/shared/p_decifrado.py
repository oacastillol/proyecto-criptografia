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

def pdecifrado(message, key):
    #print ('mensaje: ',message, " key ",key)
    #Paso a cada letra y numero a ascii
    estatico = gimg1859()
    #list1 = d_ascii(message)
    list1 = [35, 8, 24, 13, 181, 189, 160, 160]


    list2 = d_ascii(key)
    #[1, 253, 1, 253, 147, 158, 147, 158] mensaje cifrado
    #clave
    #Etapa inicial del Algoritmo gimg1859
    #print ("Estatico : ", estatico, "list1 ",list1)
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
    d = d_caracter(d_2)
    #lo muestra lo que vale en ascii
    print ('decifrado en ascii',d_2)
    #print('2',l_2,r_2)
    return (str(d))
#MAIN
#tupla inmutable [103, 105, 109, 103, 49, 56, 53, 57]
#estatico = list('gimg1859')
message = list('vanegask')
key = list ('moralesk')
#r = 'r'
#l = 'l'
#keyGen = keyGenerator(key, 5)
#nzk = list(d_ascii(key))
#print (nzk)
#cbloque = d_bloque(nzk,l)
#cbloque1 = d_bloque(nzk,r)
#union = d_unir(cbloque,cbloque1)
#print ('bloque ',cbloque,cbloque1)
#print ('union ' ,union)
#print ('---------------')
#esta = gimg1859()
#print (" es gimg" ,esta)
#ant = pdecifrado(message,key)
#print ('decifrado gimg1859: ' ,ant)
#dcorrimiento = d_corrimiento(message)
decifrado = pdecifrado(message,key)
#print('decifrado: ',decifrado)
dcaracter = d_caracter([1, 253, 1, 253, 147, 158, 147, 158] )
#print ('mensaje :' ,dcaracter)
