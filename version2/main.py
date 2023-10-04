import faust
from decouple import config
import json
import numpy as np
from push_data_mongo import push_dataFull as push_dataFull_mongo
from push_data_mysql import push_to_sql
# Configuración sencilla de Faust utilizando la configuración importada
app = faust.App(
    config("BROKER_URL"),
    broker=config("COMSUMER"), 
    value_serializer=config("FORMAT"),
)

topic = app.topic(config("TOPIC"))

array_IPv4 = []
array_passport = []
array_city = []
arra_name = []
array_company =  []
total_data = []

def processData(data):
    try:
        total_data.append(data)
        if "city" in data:
            array_city.append(data)
        elif "company" in data:
            array_company.append(data)
        elif "name" in data:
            name = data.get("name", "")
            last_name = data.get("last_name", "")
            data['fullname'] = f"{name} {last_name}"
            # Elimino las columnas
            del data['name']
            del data['last_name']
            arra_name.append(data)
        elif "IBAN" in data:
            array_passport.append(data)
        elif "IPv4" in data:
            array_IPv4.append(data)
        else:
            pass
        
        
        for item_name in arra_name:
            passport_item_name = item_name.get("passport")
            
            for item_pasport in array_passport:
                passport_item_passport = item_pasport.get("passport")
                if passport_item_name == passport_item_passport:
                    passport_item_passport = item_pasport.get("passport")
                    name_item_name = item_name.get("fullname")
                    item_name = item_name
                    item_passport = item_pasport
                    
                    for item_city in array_city: 
                        fullname_item_city = item_city.get("fullname")
                        if fullname_item_city == name_item_name:
                            address_item_city = item_city.get("address")
                            
                            for item_company in array_company:
                                fullname_item_company = item_company.get("fullname")
                                if fullname_item_company == fullname_item_city:
                                    
                                    for item_ipv4 in array_IPv4:
                                        address_item_ipv4 = item_ipv4.get("address")
                                        if address_item_city == address_item_ipv4:
                                            data_full = [item_name, item_city, item_company, item_passport, item_ipv4] 
                                            arra_name.remove(item_name)
                                            array_city.remove(item_city)
                                            array_company.remove(item_company)
                                            array_passport.remove(item_pasport)
                                            array_IPv4.remove(item_ipv4)
                                            
                                            data_combinada = {}
                                           
                                            for diccionario in data_full:
                                                data_combinada.update(diccionario)
                                            
                                            push_dataFull_mongo(data_combinada)
                                            push_to_sql(data_combinada)
                                            
                                            lista = {
                                                "array_name":len(arra_name),
                                                "array city":len(array_city),
                                                "array_company":len(array_company),
                                                "array_passpor":len(array_passport),
                                                "array_ipv4":len(array_IPv4),
                                                "suma total":len(arra_name) + len(array_city) + len(array_company) + len(array_passport) + len(array_IPv4),
                                                "array_toda_la_data":len(total_data),
                                            }
                                            
                                            print("****************")
                                            print(lista)
                                            print("****************")
                                            
        
    except Exception as e:
        print(e)
        pass

# faust -A main worker
# Define a Faust table to store consumed data
@app.agent(topic)
async def consume_messages(messages):
    '''Consume messages from a Kafka topic
    To start the application enter the following command: 
    faust -A main worker
    '''
    try:
        async for message in messages:
            data = message
            processData(data)
            # print(f'Received message: {data}')
    except Exception as e:
        # print(e)
        pass
    
    # print("**************************")
    # print(item_name)
    # print(item_city)
    # print(item_company)
    # print(item_passport)
    # print(item_ipv4)
    # print("**************************")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # with open("datos.json", "w") as archivo:
        #     json.dump(data_full, archivo)
        #     archivo.write('\n')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#         import faust
# from decouple import config
# import json
# import numpy as np
# from push_data import push_dataFull
# # Configuración sencilla de Faust utilizando la configuración importada
# app = faust.App(
#     config("BROKER_URL"),
#     broker=config("COMSUMER"), 
#     value_serializer=config("FORMAT"),
# )

# # Define a Kafka topic to consume from
# topic = app.topic(config("TOPIC"))
# address = {}
# array_IPv4 = []
# array_passport = []
# array_fullname = []
# arra_name = []
# # faust -A main worker

# def processData(data):
#     try:
#         if "fullname" in data:
#             array_fullname.append(data)
#         elif "name" in data:
#             name = data.get("name", "")
#             last_name = data.get("last_name", "")
#             data['fullname'] = f"{name} {last_name}"
#             # Elimino las columnas
#             del data['name']
#             del data['last_name']
#             arra_name.append(data)
#         elif "IBAN" in data:
#             array_passport.append(data)
#         elif "IPv4" in data:
#             array_IPv4.append(data)
#         else:
#             pass
        
#         for item_name in arra_name:
            
#             passport_item_name = item_name.get("passport")
            
#             for item_pasport in array_passport:
#                 passport_item_passport = item_pasport.get("passport")
#                 if passport_item_name == passport_item_passport:
#                     passport_item_passport = item_pasport.get("passport")
#                     name_item_name = item_name.get("fullname")
#                     item_name = item_name
#                     item_passport = item_pasport
        
#                     for item_fullname in array_fullname: 
#                         fullname_item_fullname = item_fullname.get("fullname")
#                         if fullname_item_fullname == name_item_name:
#                             #pregunto si fullname tiene company
#                             if "address" in item_fullname:
#                                 address_item_fullname = item_fullname.get("address")
#                                 for item_ipv4 in array_IPv4:
#                                     address_item_ipv4 = item_ipv4.get("address")
#                                     if address_item_fullname == address_item_ipv4:
#                                         print("***********")
#                                         print(item_name)
#                                         print(item_fullname)
#                                         print(item_passport)
#                                         print(item_ipv4)
#                                         print("************")
#                             else:
#                                 print("------------")
#                                 print(item_name)
#                                 print(item_fullname)
#                                 print(item_passport)
#                                 print("-------------")
                                
                        
                               
                                
                                
                                
                                
                                
                                
                           
                            
                            
                                  
                    
            
        
#     except Exception as e:
#         # print(e)
#         pass

# # faust -A main worker
# # Define a Faust table to store consumed data
# @app.agent(topic)
# async def consume_messages(messages):
#     '''Consume messages from a Kafka topic
#     To start the application enter the following command: 
#     faust -A main worker
#     '''
#     try:
#         async for message in messages:
#             data = message
#             processData(data)
#             # print(f'Received message: {data}')
#     except Exception as e:
#         # print(e)
#         pass
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     # with open("datos.json", "w") as archivo:
#         #     json.dump(data_full, archivo)
#         #     archivo.write('\n')