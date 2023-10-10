# Librerías para conectar con Kafka
import subprocess
import time

# Comando para iniciar ZooKeeper
zookeeper_command = "/Applications/kafka-3.5.1-src/bin/zookeeper-server-start.sh /Applications/kafka-3.5.1-src/config/zookeeper.properties"

# Comando para iniciar Kafka
kafka_command = "/Applications/kafka-3.5.1-src/bin/kafka-server-start.sh /Applications/kafka-3.5.1-src/config/server.properties"

# Iniciar ZooKeeper en un proceso separado
zookeeper_process = subprocess.Popen(zookeeper_command, shell=True)

# Esperar un momento para que ZooKeeper se inicie completamente (ajusta el tiempo según sea necesario)
time.sleep(5)

# Iniciar Kafka en un proceso separado
kafka_process = subprocess.Popen(kafka_command, shell=True)

# Esperar un momento para que Kafka se inicie completamente (ajusta el tiempo según sea necesario)
time.sleep(5)

# Cuando hayas terminado, puedes detener ZooKeeper y Kafka si es necesario
#zookeeper_process.terminate()
#kafka_process.terminate()




