import hashlib

class Encryption():
    @classmethod
    def encrypt(cls, password):
        # Utilizamos el algoritmo SHA-256 para hashear la contraseña
        hash_object = hashlib.sha256(password.encode())
        hashed_password = hash_object.hexdigest()
        return hashed_password

    @classmethod
    def verify(cls, password, hashed_password):
        # Hasheamos la contraseña ingresada y comparamos con la contraseña hasheada almacenada
        return Encryption.encrypt(password) == hashed_password

print (Encryption.encrypt("password"))
print (Encryption.verify("password", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"))

