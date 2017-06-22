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
      * LuzSensor.py
      * PresionSensor.py

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
mosquitto_sub -h eu.thethings.network -t '<AppId/devices/<DevID>/up' -u '<AppID>' -P '<AppKey>' -v
```
Todos los campos a rellenar pueden ser encontrados en la descripción de la app
creada en TTN.

### Publicación


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
