from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

data = "235451".encode("utf-8")
file_out = open("Profile Storage\Eddard Stark Profile\Profile_EQR51D3.bin", "wb")
print(file_out)
recipient_key = RSA.import_key(open("Key Storage\Eddard Stark\TPUBK51D3.pem").read())
session_key = get_random_bytes(16) #your session key here

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key) #public key = recipient_key
enc_session_key = cipher_rsa.encrypt(session_key) #session key has been encrypted

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX) #session key is brought to here
ciphertext, tag = cipher_aes.encrypt_and_digest(data) #data is encrypted with cipher_aes (session key)
[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

print("Encryption successfully.")