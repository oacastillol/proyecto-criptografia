import json
import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


message = {
    'iss': 'https://example.com/',
    'sub': 'yosida95'
}
with open('private.txt', 'r') as fh:
    signing_key = "\n".join([l.lstrip() for l in fh.read().split("\n")])
compact_jws = jwt.encode(message, signing_key, 'RS256')
print (compact_jws)

with open('public.txt', 'r') as fh:
    public_key = "\n".join([l.lstrip() for l in fh.read().split("\n")])
salida = jwt.decode(compact_jws,public_key,'RS256')
print(salida)
