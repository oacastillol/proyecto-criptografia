# Proyecto ICIS 2018_2 #

## Grupo D ##

El desarrollo se encuentra basado en [el tutorial](https://www.codementor.io/olawalealadeusi896/restful-api-with-python-flask-framework-and-postgres-db-part-1-kbrwbygx5)
se implementara el Algoritmo DES y se usara postgres como base de datos
para ejecutar debe hacer la fase de preparacion que se encuentra en el tutorial
en el archivo [variablesEntorno.sh](./variablesEntorno.sh) se encuentran las variables de entorno, sea cuidadoso al modificarla
después de usar `pipenv shell`  ejecute `. ./variablesEntorno.sh` para que el servidor tome los valores especificados.

En la carpeta **shared** ubicar las implementaciónes de los algoritmos de cifrado

Se Desarrollo el RestAPI para la aplicación, a continuación listo los endpoints:



| url                          | metodo   | descripcion                               | request                                                    | response                     |
|------------------------------|----------|-------------------------------------------|------------------------------------------------------------|------------------------------|
| /api/v1/users                | `POST`   | Crear un nuevo usuario                    | **BODY** username, password                                  | **BODY** 'jwt_token'           |
| /api/v1/users                | `GET`    | Lista los usuarios registrados            | **HEADERS** api-token                                        | **BODY** lista de usuarios     |
| /api/v1/users/login          | `POST`   | Logea al usuario                          | **BODY** username, password                                  | **BODY** 'jwt_token'           |
| /api/v1/users/:user_id       | `GET`    | devuelve la información de un usuario     | **HEADERS** api-token                                        | **BODY** userModel             |
| /api/v1/users/me             | `GET`    | información del usuario logeado           | **HEADERS** api-token                                        | **BODY** userModel             |
| /api/v1/users/me             | `PUT`    | Modifica la información de usuario actual | **HEADERS** api-token, *BODY* username, password             | **BODY** userModel             |
| /api/v1/users/me             | `DELETE` | Elimina el usuario actual                 | **HEADERS** api-token                                        | **CODE** 204                   |
| /api/v1/messages             | `POST`   | Guarda un mensaje del usuario logeado     | **HEADERS** api-token, *BODY* title, cipher                  | **BODY** messageModel          |
| /api/v1/messages             | `GET`    | Lista los mensajes del usuario loggeado   | **HEADERS** api-token                                        | **BODY** Lista de messageModel |
| /api/v1/messages/:message_id | `GET`    | Muestra un mensaje                        | **HEADERS** api-token *ROUTE* message_id                     | *BODY* messageModel          |
| /api/v1/messages/:message_id | `PUT`    | Modificar un mensaje guardado             | **HEADERS** api-token *ROUTE* message_id **BODY** messageModel | *BODY* messageModel          |
| /api/v1/messages/:message_id | `DELETE` | Eliminar un mensaje del usuario logeado   | **HEADERS** api-token *ROUTE* message_id                     | **CODE**   204                 |
| /api/v1/cipher/encode        | `POST`   | Cifrar un mensaje                         | **BODY** type:{DES,TEAM},message,key                         | **BODY** cipher                |
| /api/v1/cipher/decode        | `POST`   | Descifrar un mensaje                      | **BODY** type:{DES,TEAM},message,key                         | **BODY** message               |


