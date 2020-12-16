from cryptography.fernet import Fernet

def genratePassKey():
    key = Fernet.generate_key()
    print(key)
    print(type(key))
    abc = open("PasswordKey.key",'wb')
    abc.write(key)
    abc.close()

genratePassKey()


def getMyKey():
    abc = open("PasswordKey.key",'rb')
    return abc.read()

getMyKey()


def getContentFromUser():
    return input("Enter the Content you want to Encrypt in your python Script")

getContentFromUser()
