// Load RSA module from forge library - there is a forge.min.js in this same folder
// https://github.com/digitalbazaar/forge
let rsa = forge.pki.rsa;

// Our public key used in PEM format
// This key was generated before and should be used to encrypt all messages
let publicKeyPemFormat = '-----BEGIN PUBLIC KEY-----\
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgFX+bUlLxnHEIHLOSRRZ9Az0Y3py\
cCmwpgopNUvcJVUd4mLJG/7tH0EC0BDIQVa1yEq7+JySkZ9FxHb1rdja8f2649VA\
QARyabtFqmU+HK1kMOqZ94+NfV2xPqxev42GygeQCZT5q6i8qCF/WDhJMwFOHLlR\
sn5xhJvH2xZhFTo7AgMBAAE=\
-----END PUBLIC KEY-----'

// Load the key
let publicKey = forge.pki.publicKeyFromPem (publicKeyPemFormat);

function encrypt_text (){
  // let data = document.getElementById('text_normal').value;
  data = {'gary': 1, 'bryan': 2, 'marc': 3, 'damian':4};
  return encrypt (data);
}

function send_data_to_server (data){
  console.log (data);

  // Chrome and other browsers do not let me to POST to localhost
  // During test, use a chrome extension called postman
  // https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop
  $.post ('http://localhost:5000/decrypt', {'data': data} );
}

/* Data should contain voting order
data = {
  'gary': 1,
  'bryan': 2,
  'marc': 3,
  'damian': 4 
}

This object (data) will be serialized to json using JSON.stringify and then encrypted.
*/
function encrypt (data){

  // Serialize data to JSON
  let text = JSON.stringify (data)

  // Encryption is done using RSA-OAEP
  let ciphertext = publicKey.encrypt(text, 'RSA-OAEP');

  // Transform ciphertext to base64 encoding format
  let b64Text = forge.util.encode64(ciphertext);

  console.log (b64Text);

  return send_data_to_server(b64Text);
}