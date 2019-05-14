import requests

#response = requests.get('http://127.0.0.1:5000/user/check?ID_Employee=2001&Employee_Name=Moore') # check employee
response = requests.get('http://127.0.0.1:5000/user/checkHash?QR_Code=99700&Record_Hashing=d5a1516fd1113f94f036204bcd5c33d6c1c1016afde8a2e7dd6fda18493f3bc7')
#response = requests.get('http://127.0.0.1:5000/user/hash?Trainee_ID=2001&QR_Code=99700')
a = response.content

b= a.decode('utf-8')
b = b.replace('"','')
print(b)
print(type(b))
b = int(b)

if b == 1:
    print("true hash.")
elif b == 0:
    print("false hash.")
