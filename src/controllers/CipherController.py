from flask import request, g, Blueprint, json, Response

cipher_api = Blueprint('cipher_api', __name__)

@cipher_api.route('/encode',methods=['POST'])
def encode():
    """
    Cipher message
    """
    req_data = request.get_json()
    if req_data['type'] == "DES":
        return custom_response({"message":"cipher des"},200)
    else:
        return custom_response({"message":"cipher team Method"},200)

@cipher_api.route('/decode',methods=['POST'])
def decode():
    """
    Decode message
    """
    req_data = request.get_json()
    if  req_data['type'] == "DES":
        return custom_response({"message":"decode des"},200)
    else:
        return custom_response({"message":"decode team method"},200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
)
