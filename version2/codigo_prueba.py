        
        
# import faust
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