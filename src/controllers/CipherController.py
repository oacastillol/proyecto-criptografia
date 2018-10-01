from flask import request, g, Blueprint, json, Response, jsonify,render_template
from ..shared.DESCipher import DES
from ..shared.p_cifrado import pcifrado
from ..shared.p_decifrado import pdecifrado
cipher_api = Blueprint('cipher_api', __name__)
test = '123'
@cipher_api.route('/encode',methods=['POST'])
def encode():
    """
    Cipher message
    """
    req_data = request.get_json()
    exist = 'type' not in req_data or 'message' not in req_data or 'key' not in req_data
    void = not exist and (req_data['type'] == '' or req_data['message'] == '' or req_data['key'] == '')
    if exist or void:
          return custom_response({'error': 'se requiere un mensaje una llave y un tipo para cifrar'}, 400)
    else:
        message = req_data['message']
        key = req_data['key']
        tipo = req_data['type']
    if tipo == "DES":
        cipher = DES(message,tipo,'cipher');
        return  custom_response({"message":cipher},200)
    else:
        cipher = pcifrado(message,tipo);
        return  custom_response({"message":cipher},200)


@cipher_api.route('/decode',methods=['POST'])
def decode():
    """
    Decode message
    """
    req_data = request.get_json()
    exist = 'type' not in req_data or 'message' not in req_data or 'key' not in req_data
    void = not exist and (req_data['type'] == '' or req_data['message'] == '' or req_data['key'] == '')
    if exist or void:
          return custom_response({'error': 'se requiere un mensaje una llave y un tipo para descifrar'}, 400)
    else:
        message = req_data['message']
        key = req_data['key']
        tipo = req_data['type']
    if  tipo == "DES":
        cipher = DES(message,key,'descipher')
        return custom_response({"message":cipher},200)
    else:
        cipher = pdecifrado(message,key)
        return custom_response({"message":cipher},200)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
)
