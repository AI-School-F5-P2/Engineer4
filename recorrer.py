import json


with open('datos3.json', 'r') as archivo_json:
    # Inicializa un diccionario para almacenar los datos de los usuarios
    usuarios = {}

    # Itera sobre cada línea del archivo JSON
    for linea in archivo_json:
        # Carga el diccionario desde la línea
        diccionario = json.loads(linea)

        # Obtén el número de pasaporte o una clave única que identifique al usuario
        clave_usuario = diccionario.get("address")  # Cambia a la clave adecuada si es diferente

        # Verifica si ya existe un usuario con la misma clave
        if clave_usuario in usuarios:
            # Si existe, combina los datos del usuario actual con los existentes
            usuario_existente = usuarios[clave_usuario]
            for clave, valor in diccionario.items():
                # Agrega nuevos datos y no reemplaza los existentes
                if clave not in usuario_existente:
                    usuario_existente[clave] = valor
        else:
            # Si no existe, crea un nuevo usuario con los datos actuales
            usuarios[clave_usuario] = diccionario
            
            
for clave_usuario, datos_usuario in usuarios.items():
    print(f"Usuario con clave {clave_usuario}:")
    print(datos_usuario)