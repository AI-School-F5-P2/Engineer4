# Ejemplo de datos JSON simulados en una lista de diccionarios
datos_json = [
    {"nombre": "Juan Pérez", "teléfono": "555-123-4567", "email": "juan@example.com"},
    {"nombre": "Ana García", "teléfono": "555-987-6543", "email": "ana@example.com"},
    {"nombre": "Juan Pérez", "teléfono": "555-111-2222", "email": "juanp@example.com"},
    {"nombre": "Carlos Sánchez", "teléfono": "555-333-4444", "email": "carlos@example.com"},
]

# Diccionario para almacenar registros duplicados
registros_duplicados = {}

# Iteramos sobre los datos y buscamos duplicados basados en el nombre
for dato in datos_json:
    nombre = dato["nombre"]
    if nombre in registros_duplicados:
        registros_duplicados[nombre].append(dato)
    else:
        registros_duplicados[nombre] = [dato]

# Imprimir registros duplicados
for nombre, registros in registros_duplicados.items():
    if len(registros) > 1:
        print(f"Registros duplicados para '{nombre}':")
        for registro in registros:
            print(registro)
        