""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import LoRa
import socket
import binascii
import struct
import time
from pysense import Pysense
from GestionSensores import Gestion
import machine
from machine import Timer
#------------------------------------------------------------------------------#
# Función encargada de crear la cadena en formato JSON con los datos de los
# sensores medidos y publicarla vía LoRa a TTN.
def publicarJSON(alarmaPub):
    try:
        print("Creando JSON")
        json = gestion.crearjson()
    except 0:
        return
    s.send(json[0])
#------------------------------------------------------------------------------#
#Callback para evento de recepción LoRa
def recbLora(lora):
    #TODO: Recibirá los datos en forma hexadecimal. Se debe desarrollar un
    #método para decodificar el mensaje y modificar los parámetros.
    


#------------------------------------------------------------------------------#
# Configuración e Inicio de la conexión vía LoRaWAN con el network Server TTN
# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)
print('LoRa MAC:' + binascii.hexlify(lora.mac()).upper().decode('utf-8'))
# create an OTA authentication params
#ID del dispositivo. Es la dirección LORA_MAC (puede ser cualquier número)
dev_eui = binascii.unhexlify('70 B3 D5 49 9D AE C6 EA'.replace(' ',''))
#ID de la app. (Seleccionada por el usuario)
app_eui = binascii.unhexlify('70 B3 D5 7E F0 00 42 A4'.replace(' ',''))
#Clave de la app para realizar el handshake. Única para cada dispositivo.
app_key = binascii.unhexlify('36 93 92 6E 05 B3 01 A5 02 AB CF CA 43 0D A5 2A'.replace(' ',''))

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')
print('Joined!!!')
# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
s.setblocking(False)

lora.callback(trigger = LoRa.RX_PACKET_EVENT,handler = recbLora, arg = s.recv(256))  #256 = Buffer Size

time.sleep(5.0)
#------------------------------------------------------------------------------#
# Código propio para lectura y publicación de valores de sensores
#Crea una instancia de la clase que gestiona los sensores
gestion = Gestion()
time.sleep(4.0)
intervalopub = gestion.intervaloMinimo()
print("Intervalo de Publicacion: %d segundos"  %(intervalopub))
# Fija la alarma de publicación de datos con el intervalo mínimo de los intervalos
# de publicación.
alarmaPub = Timer.Alarm(publicarJSON, intervalopub, periodic=True)
#------------------------------------------------------------------------------#
# FIN PROGRAMA
