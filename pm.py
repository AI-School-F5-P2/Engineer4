from classes.mongo_db import UseMongo
from config.mongo_conn import mongo_data
from config.mongo_use import mongo_use

mi_cliente = UseMongo(
    server=mongo_data['server'], 
    port=mongo_data['port'], 
    user=mongo_data['user'], 
    password=mongo_data['password']
)

mi_cliente.select_db(mongo_use['db'])
mi_cliente.select_col(mongo_use['collection'])

argumentos = ['moto', 100, '1000cc']
documentos = [
    {"nombre": "Harry", "telefono": '400500600', 'cargo': 'Director'},
    {'persona': 'León', 'pasaporte': 'XFR-04502', 'status': 'autorizado'},
    {'vehiculo': '%s', 'potencia': '%s', 'combustible': 'gasolina', 'cubicacion': '%s'}
]
mi_cliente.insert(documentos, argumentos)
documento = {"nombre": "Ejemplo", "edad": 30}
mi_cliente.insert(documento)


print (mi_cliente.count_docs())

mi_cliente.add_index(['nombre', 'persona'])

print (mi_cliente.list_idx())




