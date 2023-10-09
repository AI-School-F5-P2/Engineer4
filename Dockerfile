# Utiliza una imagen oficial de Python 3.8 como base
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código fuente de tu proyecto al contenedor
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Instala los paquetes necesarios para PostgreSQL (puedes ajustar esto según tu base de datos)
# RUN apt-get update && apt-get install -y postgresql-client


# Define variables de entorno para la conexión a la base de datos SQL (ajusta según tu configuración)
# ENV DB_HOST=localhost
# ENV DB_PORT=5432
# ENV DB_NAME=MONGO_DATABASE
# ENV DB_USER=MONGO_user
# ENV DB_PASSWORD=

# Instala el cliente de MongoDB (puedes ajustar esto según tu base de datos)

# Define variables de entorno para la conexión a MongoDB (ajusta según tu configuración)
# ENV MONGO_URI=your-mongo-uri

# Expone el puerto de la aplicación (ajusta según tu aplicación)
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["faust", "-A", "main","worker"]
