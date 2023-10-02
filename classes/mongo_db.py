from pymongo import *
from pymongo.errors import WriteError, DuplicateKeyError

## Leemos los datos de configuración
from config.mongo_conn import mongo_data
        

class UseMongo:
    ## A NIVEL DE CLIENTE
    def __init__(self, server=mongo_data["server"], port=mongo_data["port"], user=mongo_data["user"], password=mongo_data["password"], notificaciones = False):
        # Se crea un objeto para representar una base de datos Mongo.
        # El objeto se crea con los datos pasados al constructor.
        if mongo_data["auth"]:
            self.client = MongoClient(f"mongodb://{user}:{password}@{server}:{port}/")
        else:
            self.client = MongoClient(f"mongodb://{server}:{port}/")
        # Los datos pasados al constructor se almacenan en propiedades del objeto creado.
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.notificaciones = notificaciones # Para indicar si los métodos devuelven notificaciones en caso de errores.
    
    def destroy(self):
        # Se cierra la conexión del cliente
        self.client.close()

    ## A NIVEL DE BASE DE DATOS
    def show_dbs(self):
        # Ejecuta el comando `listDatabases` y devuelve la lista de bases de datos.
        try:
            databases = self.client.list_database_names()
            return databases
        except:
            if self.notificaciones:
                return "Se ha producido un error al mostrar las bases de datos."
            else:
                return

    def select_db(self, db_name):
        # Selecciona una base de datos sobre la que se harán las operaciones.
        # No importa si no existe, porque se creará automáticamente cuando se 
        # seleccione una colección y se inserte el primer documento. 
        try:
            self.db = self.client[db_name]
        except:
            if self.notificaciones:
                print ("Se ha producido un error al seleccionar una base de datos.")
            else:
                pass
        return
    
    def remove_db(self, db_name = ""):
        # Se borra la base de datos especificada.
        # Si no se especifica ninguna, se borra la base de datos actual.
        try:
            if db_name == "":
                self.client.drop_database(self.db)
            else:
                self.client.drop_database(db_name)
        except:
            result = "Se ha producido un error al eliminar una base de datos." if self.notificaciones else ""
            print (result)
        return
    
    ## A NIVEL DE COLECCIÓN
    def get_cols(self):
        # Devuelve la lista de colecciones de una base de datos, si las hay.
        # Si no las hay, devuelve una lista vacía.
        try:
            result = self.db.list_collection_names()
        except:
            result = "Se ha producido un error al listar las colecciones." if self.notificaciones else ""
        return result
    
    def select_col(self, collection_name):
        # Selecciona una colección de la base de datos.
        # Si la colección no existe se creará automáticamente 
        # cuando se inserte el primer documento.
        try:
            self.collection = self.db[collection_name]
        except:
            result = "Se ha producido un error al seleccionar una colección." if self.notificaciones else ""
            print (result)
        return
    
    def remove_col(self, collection_name = ""):
        # Elimina una colección de documentos. Si no se especifica un 
        # nombre de colección elimina la colección actualmente seleccionada.
        try:
            if collection_name == "":
                self.db.drop_collection(self.collection)
            else:
                self.db.drop_collection(collection_name)
        except:
            result = "Se ha producido un error al eliminar una colección." if self.notificaciones else ""
            print (result)
    
    ## A NIVEL DE DOCUMENTO
    def count_docs(self, query = {}):
        # Cuenta los documentos de la colección actualmente 
        # seleccionada y devuelve ese valor.
        # Si se especifica una condición cuenta los documentos que la cumplen.
        try:
            result = self.collection.count_documents(query)
        except:
            result = "Se ha producido un error al contar documentos." if self.notificaciones else ""
        return result

    def select_docs(self, query = {}, one = False):
        # Recibe una consulta de selección en la sintaxis de MongoDB
        # y devuelve todos los documentos que cuamplan la consulta 
        # en una lista.
        # Si one es True busca un solo documento con find_one.
        # En caso contrario usa find.
        # En todo caso devuelve el resultado en una lista.
        try:
            if one:
                docs = [self.collection.find_one(query)]
            else:
                resultado = self.collection.find(query)
                docs = []
                for item in resultado:
                    docs.append(item)
            return docs
        except:
            result = "Se ha producido un error al seleccionar documentos." if self.notificaciones else ""
            return result
    
    def insert(self, documentos, argumentos = []):
        # Inserta uno o más documentos con la sentencia insert_many.
        # Si sólo se ha pasado un documento y no se ha pasado como 
        # lista, se convierte en lista al principio del método.
        if not isinstance(documentos, list):
            documentos = [documentos]
        for doc in documentos:
            # Si se han pasado los valores en una lista aparte de argumentos se 
            # se integran en los documentos, en el mismo orden en que se han pasado.
            for key, value in doc.items():
                if value == '%s':
                    doc[key] = argumentos.pop(0)
            try:
                self.collection.insert_one(doc)
                #print("Documento insertado:", doc)
            except DuplicateKeyError as error:
                if self.notificaciones:
                    print("Error de duplicado:", str(error)) 
                else:
                    pass
            except WriteError as error:
                if self.notificaciones:
                    print ("Se ha producido un error al insertar documento(s).")
                    print('Código de error:', error.code)
                    print('Mensaje de error:', error.details)
                else:
                    pass
        return

    def remove_docs(self, query = {}, one = False):
        # Recibe una consulta opcional para borrar documentos.
        # Si no se indica una consulta, se borra el primer documento 
        # de la colección en uso, si se indica one = True, o todos, si one es False.
        # Si se pone una query, se elimina el primer documento que la cumpla, 
        # si one = True, o todos los que la cumplan, si one = False.
        try:
            if one:
                self.collection.delete_one(query)
            else:
                self.collection.delete_many(query)
        except:
            result = "Se ha producido un error al eliminar documentos." if self.notificaciones else ""
            print (result)
        return
    
    def change_docs(self, reform, select = {}, one = False):
        # Ejecuta el método update (si one es False) o update_one (si one es True)
        # Si no se especifica select, selecciona el primer documento de la colección 
        # (o todos, si one es False).
        # Si se especifica select, selecciona el primer documento de la colección 
        # que cumpla la condición (o todos los que la cumplan, si one es False)
        try:
            if one:
                self.collection.update_one(select, {"$set": reform})
            else:
                self.collection.update_many(select, {"$set": reform})
        except:
            result = "Se ha producido un error al actualizar documentos." if self.notificaciones else ""
            print (result)
        return

    ## A NIVEL DE ÍNDICE
    def add_index(self, indexes:list, orders = [ASCENDING], uniques = [False]):
        # Crea un indice sobre la clave que se pone en index.
        # Si no se especifica orient, será ASCENDING.
        # La alternativa es DESCENDING
        if not isinstance (indexes, list):
            print ("El criterio o criterios de indexación deben ser una lista.")
            return
        if not isinstance (orders, list):
            print ("El sentido o sentidos de indexación deben ser una lista.")
            return
        if not isinstance (uniques, list):
            print ("Las unicidades de criterios de indexación deben ser una lista.")
            return
        # Si hay más órdenes de indexación que criterios recortamos la lista de ordenes de indexación
        if len(orders) > len(indexes):
            orders = orders[:len(indexes)]
        # Si hay menos órdenes de indexación que criterios, se amplían los órdenes con True.
        if len(orders) < len(indexes):
            orders.extend([ASCENDING] * (len(indexes) - len(orders)))
        # Si hay más unicidades que criterios recortamos la lista de unicidades.
        if len(uniques) > len(indexes):
            uniques = uniques[:len(indexes)]
        # Si hay menos unicidades que criterios se amplian las unicidades con False.
        if len(uniques) < len(indexes):
            uniques.extend([False] * (len(indexes) - len(uniques)))
        # Si alguno de los elementos de orders no es ASCENDING o DESCENDING lo convertimos.
        for i, value in enumerate(orders):
            if value not in [ASCENDING, DESCENDING]:
                orders[i] = ASCENDING
        # Si alguno de los elementos de uniques no es booleano lo convertimos a False.
        for i, value in enumerate(uniques):
            if not isinstance(value, bool):
                uniques[i] = False
        # A partir de las listas de indices y de órdenes creamos la lista de tuplas de indexación.
        indices = []
        for campo, direccion, unique in zip(indexes, orders, uniques):
            indice = IndexModel([(campo, direccion)], unique=unique)
            indices.append(indice)
        try:
            self.collection.create_indexes(indices)
        except Exception as e:
            # Obtener información sobre el campo y la dirección del índice
            result = f"Se ha producido un error al indexar. {str(e)}" if self.notificaciones else ""
            print (result)
        return

    def remove_idx(self, indexes:list):
        # Eliminar índices de la colección en curso.
        if not isinstance (indexes, list):
            indexes = [indexes]
        try:
            self.collection.drop_indexes()
        except:
            result = "Error al eliminar índices." if self.notificaciones else ""
            print (result)
        return
    
    def list_idx(self):
        idx = self.collection.list_indexes()
        custom_indices = []
        for index in idx:
            # Filtra los índices que no sean el índice predeterminado (_id) y los que son creados automáticamente.
            if "name" in index and index["name"] != "_id_":
                # Extrae el nombre y el sentido del índice.
                index_info = {
                    "name": index["name"],
                    "direction": [(k, v) for k, v in index["key"].items()]
                }
                custom_indices.append(index_info)
        return custom_indices