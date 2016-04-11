from flask import Flask, request, redirect, url_for, send_from_directory, jsonify

import Crypto
from Crypto.Cipher import *
from Crypto.PublicKey import RSA

import json
from base64 import b64decode

# Setup Flask app.
app = Flask(__name__, static_url_path='/static')
app.debug = True


def decrypt_data (data):
	"""
	-----BEGIN RSA PRIVATE KEY-----
	MIICWgIBAAKBgFX+bUlLxnHEIHLOSRRZ9Az0Y3pycCmwpgopNUvcJVUd4mLJG/7t
	H0EC0BDIQVa1yEq7+JySkZ9FxHb1rdja8f2649VAQARyabtFqmU+HK1kMOqZ94+N
	fV2xPqxev42GygeQCZT5q6i8qCF/WDhJMwFOHLlRsn5xhJvH2xZhFTo7AgMBAAEC
	gYBQ1KChPsq/cR0XDPQAXzVZX/aJyDvJ1DOeZXGlZr7orPh45pScIQM5to0g2Tsh
	aClmph1f/x1GWuv67Z+FsPe48tU50D44YVQGwVHnWpvVvUYuMVhBQttpIqfT12dK
	nMvuf9Ey5PW3eA+8wHYbcOwH1zUAeDj0dY/+M1V3vUkmoQJBAJs82zoA9QZbx1EY
	quMkuikYHJfiWHhxpqazUFSWSIKstBY0fWQG67tEnM99nVEDtQkLB5URbsoUDvJt
	Tiyo+ikCQQCNz6IohcEsBYqcX8HEWjbuWX6k9bqfVi9yzH56IuDHrhKF8YGDTlS9
	VpDUPv22kXxhJD8oqdGMisHL/ytS2OXDAkABap69esDBnBjHfqgghndEZLnuENyp
	zK+umbhD7VMgDh9ejIAQZ5fDD682nXjQAm6mdHlPPOd75I72W1T5R1lxAkBvO+SI
	QJJLQ3V8PygwKktYHl7WaeEexm2lcH3ss5r5RbNF2S+rnS+e7F3h/h7oq6mSUOox
	rTKvOM/Wgaqr63IdAkBtA/tws4MvZK3Rc+eCnvtv/mDLkiHx2ZiCHl5kdOd/I1Pc
	Eio5nou7ptAepdpn45NlnnIbJ3vmxThiHzfukMVq
	-----END RSA PRIVATE KEY-----
	"""

	# private key is store in this same folder at private-key.pem
	f = open ('private-key.pem', 'r');
	key = RSA.importKey(f.read());

	# Generate a new cipher with the private key
	cipher = PKCS1_OAEP.new (key);
	
	text = data.replace (' ', '+')
	ciphertext = b64decode(text)
	decrypted_text = cipher.decrypt(ciphertext)

	return json.loads(decrypted_text);

@app.route ('/')
def root():
	return app.send_static_file ('index.html');

@app.route ('/decrypt', methods=['POST'])
def decrypt():
	data = request.args.get ('data');
	print data;
	print decrypt_data(data)
	return 'OK', 202

if __name__ == '__main__':
	  app.run()