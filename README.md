# PROYECTO DATA ENGINEER: Proceso ETL
### Equipo 4


Equipo de ingenieros de datos freelance de DataTech Solutions!

Hemos sido seleccionados para abordar un proyecto crucial para nuestro cliente, HR Pro, una destacada empresa en el sector de recursos humanos. El objetivo principal de este proyecto es diseñar e implementar un sistema de gestión de datos eficiente para HR Pro, permitiéndoles organizar y analizar grandes volúmenes de información provenientes de diversas fuentes, tales como solicitudes de empleo, registros de nómina, encuestas de empleados, y más. Cada miembro del equipo aporta habilidades únicas en extracción, transformación y carga de datos (ETL), junto con experiencia en el uso de tecnologías de vanguardia como Apache Kafka, MongoDB y bases de datos SQL.


Nuestra labor involucra trabajar con una amplia variedad de datos que abarcan desde información personal hasta registros financieros y métricas de rendimiento.

### Pasos Clave


Extracción de Datos: Identificar y recopilar datos de múltiples fuentes, como bases de datos, archivos CSV, feeds en tiempo real y más. Utilizaremos tecnologías como kafka para asegurar una extracción eficiente y en tiempo real de estos datos.

Transformación de Datos: Los datos recolectados pueden variar en formato y estructura. Debemos diseñar transformaciones que los estandaricen y los hagan aptos para su posterior análisis.

Carga de Datos: Desarrollar un sistema que permita la carga de datos en una base de datos MongoDB para aquellos datos no estructurados y en un almacén de datos SQL para datos estructurados. Esto garantiza una organización eficiente y acceso rápido a la información.

Entorno Dockerizado: Implementaremos el sistema en un entorno Dockerizado para facilitar la administración, escalabilidad y portabilidad. Esto asegura que HR Pro pueda expandir su capacidad de datos sin problemas.

# ESTRUCTURA DE ARCHIVOS
 
 El proyecto contiene las siguientes carpetas:

 #### Auxiliares: 
 Recibe los mensajes de kafka, los procesa y los envia a mysql.

#### clases:
Paquete compuesto por archivo init, este se conecta a la clase de datos dependiendo de  los motores, se conecta a una u otra.

#### config: 
El archivo de configuración (`config`) es esencial para la correcta operación de nuestro sistema de gestión de datos.

#### docker-compose.yaml
Se guardan las configuraciones para hacer las conexiones a la base de datos

#### Instruccions para clonar y ejecutar este proyecto

- Git clone https://github.com/AI-School-F5-P2/Engineer4.git
- Entrar a la carpeta, instalar los requirements con pip install -r requirements.txt
- Ejectuar el comando faust -A main worker
- Tener previamente instalado mongocompass, y mongo, (automaticamente la base de datos se crea y podras visualizar los datos)
- De igual forma deberaas clonar el siguiente repp: https://github.com/DavidLeirado/data-engineering-educational-project
 que sirve a modo de extractor de datos es un composer donde tendras que seguir las intrucciones de su propio readme para continuar


## INTEGRANTES DEL EQUIPO 4

- Alexis Venegas
- Alexa Montenegro
- Maikol Garrido
- Jose 
- Rodrigo L
