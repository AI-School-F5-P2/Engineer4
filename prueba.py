import json
# DATOS FIPTICIOS
fullnames = [
    {"fullname": "Mr Perez", "city": "madrid", "address": "calle 22"},
    {"fullname": "Garry Perez", "city": "Lleida", "address": "calle 30"},
    {"fullname": "Pamela Perez", "city": "barcelona", "address": "calle 42"},
    {"fullname": "Maikol Garrido", "city": "vakencia", "address": "calle 50"},
    {"fullname": "Juan Perez", "city": "caracas", "address": "calle 52"},pppppppppp
]

name = [
    {"name": "Garry", "last_name": "Perez", "sex": ["ND"], "telfnumber": "+34 828881626", "passport": "O72781818GP", "email": "garry72@yahoo.com"},
    {"name": "Pamela", "last_name": "Perez", "sex": ["ND"], "telfnumber": "+34871841956", "passport": "P67893956PP", "email": "pamela@gmail.com"},
    {"name": "Juan", "last_name": "Perez", "sex": ["M"], "telfnumber": "09714558510", "passport": "119759331JP", "email": "juan04@hotmail.co.uk"},
    {"name": "Mr", "last_name": "Perez", "sex": None, "telfnumber": "06958496001", "passport": "S51887718MP", "email": "anthony@yahoo.co.uk"},pppppppp
  
]

passport = [
    {"passport": "119759331JP", "IBAN": "FR1863246239031849361616823JP", "salary": "169264kr"},
    {"passport": "S51887718MP", "IBAN": "GB70KMQN78443664081637MP", "salary": "35711\u0192"},
    {"passport": "O72781818GP", "IBAN": "GB67NEUG41044545062330GP", "salary": "41778.\u062f.\u0625"},
    {"passport": "P67893956PP", "IBAN": "FR9259676294967419360216877PP", "salary": "148610SM"},pppppp
]


adress = [
    {"address": "calle 22", "IPv4": "145.164.175.243"},
    {"address": "calle 30", "IPv4": "67.25.167.164"},
    {"address": "calle 42", "IPv4": "200.213.179.211"},
    {"address": "calle 50", "IPv4": "64.74.48.40"},
    {"address": "calle 52", "IPv4": "64.74.48.40"},
]







combined_names = []
for item in name:
    name = item.get("name", "")
    last_name = item.get("last_name", "")
    item['name_and_last_name'] = f"{name} {last_name}"
    # Elimino las columnas
    del item['name']
    del item['last_name']
    # agregoel nombre combinado a la lista
    combined_names.append(item)

 
names_fullNames_combined = []
for item in fullnames:
    full_name_data = item
    fullname = item.get('fullname')  # Nombre completo del empleado
    for item2 in combined_names:
        name_to_check = item2  # Nombre a verificar
        if name_to_check.get("name_and_last_name") == fullname:
            combined_dict = {**full_name_data, **item2}
            names_fullNames_combined.append(combined_dict)



name_passport_combined = []
for item in passport:
    passport_data = item
    passport_num = item.get('passport')  #numero de pasaporte
    for passport_item in names_fullNames_combined:
        passport_to_check = passport_item  # Numero a verificar
        if passport_to_check.get("passport") == passport_num:
            combined_dict = {**passport_data, **passport_item}
            name_passport_combined.append(combined_dict)



name_passport_adress_combined = []
for item in fullnames:
    direcccion_data = item
    direccion_num = item.get('address')  #direccion
    for direccion_item in name_passport_combined:
        direccion_to_check = direccion_item  # Numero a verificar
        if direccion_to_check.get("address") == direccion_num:
            combined_dict = {**direcccion_data, **direccion_item}
            name_passport_adress_combined.append(combined_dict)
            
            
for item in name_passport_adress_combined:
    print(item,"\n")
    
    





























































