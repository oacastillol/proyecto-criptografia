#Main principal
#importo funciones cifrar y decifrar gimg1859
from p_cifrado import *
from p_decifrado import *

#MAIN
mensaje = list('soy estudiante de la unal')
key = list('')
#recibo el mensaje cifrado y el tamano del mensaje original
cifrado,rango_mensaje = p_cifrado(mensaje,key)
#imprime cifrado y el rango de este
print ('cifrado: ',cifrado, (len(cifrado)))
#recibe el mensaje cifrado, la clave y el rango del mensaje original
decifrado = p_decifrado(cifrado, key,rango_mensaje)
print('decifrado en ASCII', decifrado)
caracter = d_caracter(decifrado)
print('decifrado: ',caracter, (len(caracter)))
#muestra el mensaje como string
pmensaje = p_mensaje(caracter)
print('mensaje:', (pmensaje))
