# USO DE PyMongo
En este documento vamos a hablar de la librería PyMongo de Python para uso y gestión de Bases de Datos de MongoDB.
## Introducción
Para usar PyMongo hemos creado una clase, llamada **UseMongo**, en el módulo **mongo_db**. Esta clase contiene los métodos necesarios para gestionar una base de datos MongoDB.

Esta clase añade una capa adicional entre nuestro código Python y el propio PyMongo.

La clase lee los datos de configuración de un módulo externo, en un paquete de configuración.

## Las variables de configuración
La clase está diseñada para obtener las variables de configuración de un paquete externo, así:
<code>from conf.mongo_conn import mongo_data</code>
El archivo <code>mongo_conn.py</code> tiene la siguiente estructura:
<pre>mongo_data = {
    "auth": False,
    "server": "", 
    "port" : "", 
    "user": "", 
    "password": ""
}
</pre>

La variable <code>auth</code> debe tener <code>False</code> si la línea <code>auth = True</code> está comentada en el archivo de configuración del cliente de MongoDB (lo que suele ser el estado por defecto en instalaciones nuevas). En caso de que haya sido descomentada exprofeso, esta variable deberá tener el valor <code>True</code>.

## Los métodos
Los métodos de la clase se agrupan por ámbitos de actuación sobre una base de datos MongoDB.
#### A nivel de cliente
- **Constructor (método \_\_init__)**. El método constructor es común a toda la base de datos, ya que crea el cliente para operar con todos los elementos. Recibe los datos del módulo de configuración y asigna esos datos a propiedades del objeto. Puede recibir los siguientes argumentos:
-- **<code>server</code>**. Es el nombre del servidor. Por defecto es localhost. Opcional. Si no se indica se coge por defecto el que figura en el archivo de configuración.
-- **<code>port</code>**. El número de puerto. Opcional. Si no se indica se coge por defecto el que figura en el archivo de configuración.
-- **<code>user</code>**. El nombre de usuario. Opcional. Si no se indica se coge por defecto el que figura en el archivo de configuración.
-- **<code>password</code>**.  La contraseña del usuario. Opcional. Si no se indica se coge por defecto la que figura en el archivo de configuración.
Los parámetros de autenticación (**<code>user</code>** y **<code>password</code>**) sólo se tienen en cuenta si el motor de MongoDB tiene activada la autenticación. Para ello en el archivo de configuración, **<code>/etc/mongodb.conf</code>** hay que descomentar la línea **<code>#auth = true</code>**.
- **<code>destroy</code>**. Es el método opuesto al antenrior. Destruye el cliente que se generó con el constructor. No recibe ningún argumento.

#### A nivel de base de datos
- **<code>show_dbs</code>**. Muestra las bases de datos que existen en el cliente de MongoDB. No recibe ningún argumento.
- **<code>select_db</code>**. Selecciona una base de datos. Puede que la base de datos exista o no. Si no existe, cuando se cree una colección, y dentro de esta un documento, la base de datos se incorporará al cliente. Mientras tanto, permanecerá como inexistente. Recibe el siguiente argumento:
-- **<code>db_name</code>**. El nombre de la base de datos con la que deseamos operar.
- **<code>remove_db</code>**. Elimina una base de datos. Recibe el siguiente argumento:
-- **<code>db_name</code>**. El nombre de la base de datos que deseamos eliminar. *Este argumento es opcional. Si no se especifica, se borrará la base de datos actualemnte seleccionada*.

#### A nivel de colección
- **<code>get_cols</code>**. Devuelve un listado de las colecciones que hay en la base de datos seleccionada, si las hay. Solo muestra las colecciones que tienen al menos un documento. No recibe argumentos.
- **<code>select_col</code>**. Selecciona una colección en la base de datos en uso. Recibe el siguiente argumento:
-- **<code>collection_name</code>**. El nombre de la colección que se desea seleccionar. Este argumento es obligatorio.
- **<code>remove_col</code>**. Se usa para eliminar una colección de documentos. Recibe el siguiente argumento:
-- **<code>collection</code>**. El nombre de la colección que deseamos eliminar. Este argumento es opcional. Si nom se especifica se elimina la colección actualmente seleccionada.

#### A nivel de documento.
- **<code>count_docs</code>**. Cuenta los documentos de la colección seleccionada que cumplen una condición. Recibe el siguiente argumento:
-- **<code>query</code>**. La condición en formato de query de MongoDB. Es opcional. Si no se especifica, el método cuenta todos los documentos de la colección.
- **<code>select_docs</code>**. Encuentra uno o más documentos de la colección actualmente seleccionada. Recibe dos argumentos:
-- **<code>query</code>** La condición según la cual se seleccionan los documentos, en formato de consultas de MongoDB. Este argumento es opcional. Si no se especifica, seleccionará el primer documento de la colección, o todos ellos, dependiendo del próximo argumento.
-- **<code>one</code>**. Es opcional, por defecto es False, lo que indica que se seleccionarán todos los documentos que se ciñan a la query del argumento anterior, o todos los documentos de la colección. Si se pone a True se buscará el primer documento de la colección, o el primero que cumpla con la query.
- **<code>insert</code>**. Añade uno o más documentos a la colección en curso. Recibe los siguientes parámetros:
-- **<code>documentos</code>**. Uno o más documentos para insertar. Cada documento se pasa en formato de diccionario de Python. Si hay que insertar un solo documento, este puede ir como un simple diccionario, o con ese diccionario dentro de una lista. Si hay que insertar más de un documento se incluirán en una lista de disccionarios.
-- **<code>argumentos</code>**. Los valores de los documentos pueden ir en los propios documentos, en cuyo caso este parámetro no se especificará. La alternativa es que como valores de los diccionarios se esccriba '%s', en cuyo caso los valores se metan en una lista aparte. El número de argumentos en la lista debe coincidir con los valores de los diccionarios que se hayan sustituido por '%s'.
- **<code>remove_docs</code>**. Elimina uno o más documentos de la colección actualmente seleccionada. Recibe los siguientes parámetros.
-- **<code>query</code>**. Es la condición que deben de cumplir los documentos que se vayan a eliminar. La condición, si se especifica, irá en formato de consultas de MongoDB. En ese caso, si el segundo argumento es False (o no se pone), se eliminarán todos los documentos que cumplan la query. Si el segundo argumento es True, se eliminará el primer documento que cumpla la query. Si este argumento no se especifica, se eliminará el primer documento de la colección, o todos los que hay.
-- **<code>one</code>**. Si es True, se elimina sólo un documento. Si no, se eliminan todos los documentos que cumplan la codición, o todos los de la colección.
- **<code>change_docs</code>**. Se utiliza para actualizar documentos de una colección. Recibe los siguientes parámetros.
-- **<code>select</code>**. Con este argumento se seleccionan los documentos que se van a modificar. Este argumento es opcional. Si no se especifica se buscará el primer documento de la colección (si **<code>one</code>** es *<code>True</code>*) o todos los documentos (si **<code>one</code>** es *<code>False</code>*.). Si se esspecifica esta condición, se buescará el primer docuento que cumpla la query, o todos los que la cumplan.
-- **<code>reform</code>**. Este parámetro es obligatorio. Es la query que indica lo que se va a cambiar en los registros seleccionados, en sintaxis de MongoDB. Es un diccionario que puede afectar a uno o más valores. En la sintaxis de MongoDB se omite la parte **<code>{"$set":</code>** y **<code>}</code>** que es implementado por el propio método.
-- **<code>one</code>**. Este parámetro es booleano. Si se le asigna el valor *<code>True</code>* sólo se modificará el primer documento que cumpla la condición, o el primero de la colección, si no se especifica ninguna condición. Si se asigna el valor *<code>False</code>* (o se omite) se modificarán todos los documentos que cumplan la condición, o todos los documentos de la colección, si no se aplica ninguna condición.

#### A nivel de índice.
- **<code>add_index</code>**. Crea un índice sobre los documentos de la colección seleccionada. Recibe los siguientes parámetros.
-- **<code>indexes</code>**. Es el nombre de la clave sobre la que se crea el índice
-- **<code>orders</code>**. Es una lista de valores booleanos, para indicar si cada índice es <code>ASCENDING</code> (<code>True</code>) o <code>DESCENDING</code> (<code>False</code>). Si hay menos orders que indexes la matris orders se complementa, en el método, con valores <code>False</code>.
- **<code>remove_idx</code>**. Elimina índices de una colección.
-- **<code>indexes</code>**. Recibe una lista de índices para eliminar.
- **<code>list idx</code>**. Devuelve una lista de los índices en la colección en curso.

## La sintaxis de las queries en MongoDB
Las queries en MongoDB, para seleccionar un valor mayor, iguual o menor que otro siguen una sintaxis específica. Las claves se unen a los valores con los siguientes operadores:
#### Operadores de comparación
- **<code>"$eq"</code>**. Significa "igual a". Es el operador por defecto, por defecto, por lo que puede omitirse.
- **<code>"$ne"</code>**. Significa "No igual a".
- **<code>"$gt"</code>**. Significa "Mayor que".
- **<code>"$lt"</code>**. Significa "Menor que".
- **<code>"$ge"</code>**. Significa "Mayor o igual que".
- **<code>"$le"</code>**. Significa "Menor o igual que".

#### Operadores de unión de condiciones
- **<code>"$and"</code>**. Une las dos subconsultas siguientes de forma que deban cumplirse ambas.
- **<code>"$or"</code>**. Une las dos subconsultas siguientes, de forma que deba cumplirse, al menos, una de ellas.
Por ejemplo, supongamos lo siguiente:
<pre>collection.find({
  "$and": [
    {"tipo_vehiculo": {"$ne": "moto"}},
    {"$or": [
      {"potencia": {"$gt": 150}},
      {"motor": "diesel"}
    ]
  ]
})</pre>

Esto buscará los documentos en los que el tipo de vehículo no sea "moto" y, además, se cumpla que, o bien tengan una potencia mayor que 150 o bien sean diesel.

Construir estas consultas no siempre es fácil, pero deberemos usar esta sintaxis para los métodos de la clase en los que debamos seleccionar o buscar documentos específicos.