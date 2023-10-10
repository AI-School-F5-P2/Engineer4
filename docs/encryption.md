# La clase Encryption
Esta clase se usa para encriptar contraseñas, y para verificar si una contraseña coincide con su versión encriptada, a fin de asegurarnos de que se haya introducido la contraseña correcta.

Solo tiene dos métodos estáticos (de clase), por lo que no necesita ser instanciada en un objeto.

### Encriptar una contraseña.
Para encriptar una contraseña es tan sencillo como usar el método <code>encrypt</code> de la clase, como en el siguiente ejemplo:
<code>pwd = "password"
enc_pwd = Encryption.encrypt(pwd)
print (enc_pwd) # muestra 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8</code>

### Verificar una contraseña
La contraseña encriptada se almacena en una base de datos, o un fichero de configuración externo, o similar. En el momento en que un usuario se autentique, se deberá cotejar la conttraseña que dicho usuario teclee con la que haya en la base de datos encriptada. Esto lo haremos con el método <code>verify()</code>, que devolverá True o False, según la contraseña sea correcta o no.

<code>pwd_tecleada = "password"
pwd_hasheada = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
print (Encryption.verify(pwd_tecleada, pwd_hasheada))

\# Devuelve True</code>