from jwt import encode, decode

token = encode({'name':"goke"},'gost',"HS256")
print(token)
print(decode(token, 'gost', "HS256"))
