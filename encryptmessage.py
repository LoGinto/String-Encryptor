import rsa



publicKey, privateKey = rsa.newkeys(512)

message = input("Input new message:\n")
encMessage = rsa.encrypt(message.encode(),publicKey)

with open('message.txt', 'wb') as f:
    f.write(encMessage)
with open('privateKey.pem','wb') as file:
    file.write(privateKey.save_pkcs1())
    




        