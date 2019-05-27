import requests

#response = requests.get('http://127.0.0.1:5000/user/check?ID_Employee=2001&Employee_Name=Moore') # check employee
#response2 = requests.get('http://127.0.0.1:5000/user/checkHash?QR_Code=99700&Record_Hashing=d5a1516fd11ABC13f94f036204bcd5c33d6c1c1016afde8a2e7dd6fda18493f3bc7')
response2 = requests.get('http://127.0.0.1:5000/user/hash?Trainee_ID=2001&QR_Code=99700')
a2 = response2.content

b2= a2.decode('utf-8')
b2 = b2.replace('"','')
print(b2)
print(type(b2))
b2 = int(b2)
response3 = requests.get('http://127.0.0.1:5000/user/checkHash?QR_Code=99700&Record_Hashing=d5a1516fd1113f94f036204bcd5c33d6c1c1016afde8a2e7dd6fda18493f3bc7')
a3 = response3.content
b3= a3.decode('utf-8')
b3 = b3.replace('"','')
print(b3)
print(type(b3))
b3 = int(b3)

response3 = requests.get('http://127.0.0.1:5000/user/checkHash?QR_Code=99700&Record_Hashing=d5a1516fd11ABC13f94f036204bcd5c33d6c1c1016afde8a2e7dd6fda18493f3bc7')
a3 = response3.content
b3= a3.decode('utf-8')
b3 = b3.replace('"','')
print(b3)
print(type(b3))
b3 = int(b3)