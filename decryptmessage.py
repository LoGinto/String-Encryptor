import rsa


with open('privateKey.pem','rb') as file:
    privateKeyString = file.read()
    

private_key = rsa.PrivateKey.load_pkcs1(privateKeyString)


with open('message.txt','rb') as file:
    decriptedMessage = rsa.decrypt(file.read(),private_key).decode()
print("Decrypted message:\n" ,decriptedMessage)
    
