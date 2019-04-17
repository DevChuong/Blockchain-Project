import requests
print(" Input trainee decrypted QR code : ")
name = input()
response = requests.get('http://127.0.0.1:5000/user/' + name)
a = response.content
print(a.decode('utf-8'))