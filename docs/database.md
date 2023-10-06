# La clase database

Esta clase se usa para gestionar acceso a bases de datos MySQL, PostgreSQL y SQLite 3.

### Prestaciones de la clase
- Permite seleccionar el motor deseado en el constructor. Los motores se eligen como:
1 MySQL
2 PostgreSQL
3 SQLite 3
En el constructor se puede seleccionar el servidor, el puerto, el usuario y la contraseña de acceso a base de datos.
Los valores por defecto son:
-- Motor **MySQL (1)**
-- Servidor **localhost**
-- Puerto **3306**
-- Usuario: **root**
-- Contraseña en blanco **(sin contraseña)**

- Permite crear la conexión y el cursor necesarios para gestionar una base de datos.
- Permite listar los permisos del usuario.
- Permite listar las bases de datos disponibles.
- Permite seleccionar una base de datos. Si no existe, la crea en el momento de seleccionarla.
- Permite listar las tablas disponibles en la base de datos seleccionada.
- Permite efectuar los cuatro tipos básicos de consultas (Creación, Lectura, Actualización y Borrado), lo que permite establecer un CRUD completo.
- Permite efectuar consultas directas, pero también consultas preparadas para evitar riesgos de inyección SQL.

### Dependencias
Para poder emplear la clase es necesario contar en el proyecto Python con las siguientes bibliotecas:
- mysql-connector
- psycopg2
- sqlite3

Las dependencias se instalan con:
- <code>pip install mysql-connector</code>
- <code>pip install psycopg2</code>
<pre>La biblioteca sqlite3 no necesita ser intalada, ya que es nativa de Python.</pre>

### Instanciación de la clase.
Para usar la clase es necesario instanciarla en un objeto de base de datos que será el que usemos para las operaciones pertinentes. La forma básica de crear un objeto es:
<code>objeto_db = DBAccess()</code>

Esto creará un objeto de acceso a base de datos con los valores por defecto establecidos en el constructor, que hemos listado en la sección **Prestaciones de la clase**.

**Atención.** Los datos de conexión se han quitado de la clase para que se importen de un archivo extenrno de configuración.

Si necesitamos crear un objeto con otra configuración podremos pasar los parámetros necesarios en el consructor, así:
<code>objeto_db = DBAccess(engine = "2", host = "servidor.com", port = "5432", user = "user", password = "password")</code>

No hace falta pasar todos los argumentos. Solo aquellos que necesitemos diferentes de los que implementa el constructor por defecto.

### Preparando el objeto
Una vez instanciada la clase con los valores necesarios, hay que crear una conexión y un cursor. Lo haremos así:
<code>objeto_db.create_connection()</code>
<code>objeto_db.create_cursor()</code>

### Uso del objeto
El objeto de la clase DBAccess implementa todas las funcionalidades necesarias para gestionar las operaciones sobre una base de datos.
#### Ver los permisos del usuario
Un dato importante a la hora de trabajar con bases de datos es conocer los permisos que tiene el usuario que hayamos seleccionado en el constructor. Eso lo podemos hacer así:
<code>objeto_db.show_user_grants()</code>
Esto nos mostrará todos los permisos sobre las operaciones que podemos llevar a cabo.
#### Listar las bases de datos
Esto lo podemos hacer con la siguiente instrucción:
<code>objeto_db.show_databases</code>
Esto nos devolverá una lista de python con todas las bases de datos disponibles en el servidor elegido, que se gestionen con el motor que hayamos seleccionado.
#### Seleccionar una base de datos.
Una vez listadas las bases de datos podemos seleccionar una, con el siguiente mandato:
<code>objeto_db.select_database("nombre_de_la_bd_seleccionada")</code>
Si la base de datos seleccionada existe, se seleccionará. Si no existe, se crea automáticamente, y queda seleccionada.
#### Listar las tablas
Una vez seleccionada una base de datos, el siguiente paso lógico es conocer las tablas que tiene. Podemos hacer esto con la siguiente instrucción:
<code>objeto_db.show_tables()</code>
Si la base de datos existía previamente, es posible que ya tenga tablas. En ese caso, obtendremos una lista con los nombres de dichas tablas. Si la base de datos es de nueva creación, no tendrá tablas. En ese caso obtendremos una lista vacía.
#### Crear una tabla
Una de las instrucciones que podemos llevar a cabo es crear una tabla en la base de datos seleccionada. Eso lo haremos definiendo la oportuna consulta, y luego ejecutándola a través del método <code>set_data(consulta)</code> del objeto con el que estemos trabajando. A continuación mostramos un ejemplo de esto:
<code>query = '''
      CREATE TABLE carreras (
      id INT AUTO_INCREMENT PRIMARY KEY,
      fecha_hora DATETIME,
      importe FLOAT(7,2)
      );
'''
objeto_db.set_data(query)
</code>
** ATENCIÓN. La consulta mostrada en el ejemplo es para MySQL. En caso de usar otro motor de base de datos, la sintaxis SQL podría ser diferente.**
#### Obtener un recordset
Podemos ejecutar consultas de selección de datos sobre una o más de las tablas de la base de datos. Lo podemos hacer del siguiente modo:
<code>tabla = "tabla_usuarios"
columnas = ["nombre", "edad"]
id_a_buscar = 4
columnas_placeholder = ', '.join(['%s'] * len(columnas))
query = f"SELECT {columnas_placeholder} FROM {tabla} WHERE id = %s"
params = columnas + [id_a_buscar]

\# Ejecutar la consulta:
resultado = objeto_db.get_data(query, params)</code>
En <code>resultado</code> obtendremos los datos buscados si existen.
** ATENCIÓN. La consulta mostrada en el ejemplo es para MySQL. En caso de usar otro motor de base de datos, la sintaxis SQL podría ser diferente.**
#### Otras consultas
Además de consultas de recuperación de datos, podemos ejecutar consultas de inserción, actualización y borrado de datos, con el método <code>set_data(query, params)</code> del objeto.
Por ejemplo, supongamos que en la tabla de usuarios que hemos usado en el ejemplo anterior queremos insertar un nuevo registro. Lo haríamos así:
<code>\# Datos del nuevo usuario
nuevo_usuario = {
    'nombre': 'Juan Pérez',
    'edad': 30,
    'cargo': 'Analista'
}
\# Construir la consulta preparada
columnas = ', '.join(nuevo_usuario.keys())
valores_placeholder = ', '.join(['%s'] * len(nuevo_usuario))
query = f"INSERT INTO tabla_usuarios ({columnas}) VALUES ({valores_placeholder})"
params = list(nuevo_usuario.values())

\# Ejecutar la consulta
objeto_db.set_data(query, params)</code>

Para hacer una consulta de actualización, lo haríamos del mismo modo:
<code>\# Datos para la actualización
tabla = "tabla_usuarios"
campo_a_actualizar = "cargo"
nuevo_valor = "Gerente"
campo_dni = "dni"
valor_dni = "333FFF"

\# Construir la consulta preparada
query = f"UPDATE {tabla} SET {campo_a_actualizar} = %s WHERE {campo_dni} = %s"
params = [nuevo_valor, valor_dni]

\# Ejecutar la consulta
objeto_db.set_data(query, params)</code>

Por último, supongamos que queremos eliminar uno o más registros de la tabla. Lo haremos así:
<code>\#Definimos los campos y el nombre de la tabla
tabla = "tabla_usuarios"
campo = "edad"
\# Definimos los parámetros (en este caso, la edad)
params = [65]
\# Definimos la consulta
query = f"DELETE FROM {tabla} WHERE {campo} > %s"
\# Ejecutamos la consulta
objeto_db.set_data(query, params)</code>
** ATENCIÓN. Las consultas mostradas en los ejemplos son para MySQL. En caso de usar otro motor de base de datos, la sintaxis SQL podría ser diferente.**


