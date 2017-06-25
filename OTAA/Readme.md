README
================================================================================
Esta carpeta una app desarrollada para Lopy + Pysense, en la cual se leen los
sensores disponibles en la placa de forma períodica y se publican en formato
JSON vía LoRaWAN.  
Para conseguir la conectividad vía LoRaWan se ha hecho uso de otro dispositivo
Lopy con el software lorananogateway también disponible en este repositorio.  
El objetivo de este archivo es explicar la estructura de esta app y dar las
instrucciones necesarias para configurar el dispositivo Lopy para realizar la
conexión con éxito primero con el Network Server TTN y posterirormente con el
cloud vía MQTT.

__IMPORTANTE__

Tutoriales de inicio:
* https://github.com/ttn-liv/devices/wiki/Getting-started-with-the-PyCom-LoPy
* https://docs.pycom.io/pycom_esp32/index.html


Arquitectura de la app
--------------------------------------------------------------------------------
La app se puede dividir en dos grupos, archivos de programa y librerías de control
de sensores. El árbol de archivos es el siguiente:  
* OTAA->  
    * boot.py (Inicia y selecciona el archivo main)  
    * Lectura_Sensores_0.py (Pruebas de Sensores)  
    * otaa_node_0.py (conexión con TTN)  
    * LibreríaSensores ->
      * GestionSensores.py
      * HumedadSensor.py  
      * SI7006A20.py
      * LuzSensor.py  
      * LTR329ALS01.py
      * PresionSensor.py  
      * MPL3115A2.py

Los tres primeros archivos deben ir colocados en la raíz del sistema de archivos
del módulo LoPy (/flash). Los archivos de la carpeta "Librería Sensores" serán colocados
en la ruta /flash/lib (Método de trasnferencia de archivos al final).  
El archivo boot.py selecciona cuál será el archivo que contenga el código principal
del programa. Se puede seleccionar _otaa\_node\_0.py_ (programa principal) o _Lectura
\_Sensores\_0.py_ (código prueba) comentando/descomentando un par de líneas.  

MQTT
--------------------------------------------------------------------------------
Para comprobar si el dispositivo y el Network Server están enviando los mensajes
 de forma corrrecta así como enviar mensajes downlink, se puede configurar Mosquitto
de la siguiente forma:

__ATENCIÓN!! TODAS ESTAS ÓRDENES ESTÁN CONFIGURDAS PARA USAR THETHINGSNETWORK COMO
NETWORK SERVER__

### Subscripción
```
mosquitto_sub -h eu.thethings.network:1883 -t '<AppId/devices/<DevID>/up' -u '<AppID>' -P '<AppKey>' -v
```
Todos los campos a rellenar pueden ser encontrados en la descripción de la app
creada en TTN.

### Publicación
La publicación se realizará a través del broker privado hacia el Network Server.
A partir de Network Server o más concretamente desde el Gateway, el protocolo MQTT
será sustituido a LoRaWAN, disminuyendo el payload a un vector de números con un orden y un significado concreto y conocido.

CONFIGURACIÓN NANOGATEWAY
-------------------------------------------------------------------------------
Para configurar el dispositivo LoPy que actuará como NanoGateway, solo hay que comentar/descomentar algunas líneas del archivo _config.py_. Las líneas corresponden a la configuración de ID Gateway, dirección del Network Server y puerto de entrada/salida del Netwoek Server, para los dos servidores utilizados: The Things Network y Loriot.
Es importante mencionar que dado que el gateway hace uso de la conexión Wifi del dispositivo, una vez configurado ya no se estará accesible esta red y por lo tanto el servidor FTP tampoco. Para accerlo accesible de nuevo se ha de conectar el pin P12(G28) a 3V3 al durante los 1-3 primeros segundos del inicio del dispositivo, y luego retirar el puente hecho. Esta acción cargará la configuración del firmware base del dispositivo.

USO SEVER FTP (Paso archivos a LoPy)
--------------------------------------------------------------------------------
Para pasar archivos a LoPy solo hay que conectarse a su punto WiFy propio y configurar
un cliente FTP (e.g Filezilla) con las siguientes propiedades:  
* Host : 192.168.4.1
* User: micro
* Password: python
* Only use plain FTP (insecure)
* Transfer Mode: Passive

Si no aparece el punto WiFy se tiene que poner la placa en modo seguro llevando
la entrada G28 a 3V3 (solo con expansion Board).
