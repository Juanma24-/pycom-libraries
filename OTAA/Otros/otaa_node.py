""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import LoRa
import socket
import binascii
import struct
import time
# Librerias necesarias del sensor de Temperatura
from machine import Pin
from onewire import OneWire
from onewire import DS18X20

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)
print('LoRa MAC:' + binascii.hexlify(lora.mac()).upper().decode('utf-8'))

# create an OTA authentication params
dev_eui = binascii.unhexlify('70 B3 D5 49 9D AE C6 EA'.replace(' ',''))
app_eui = binascii.unhexlify('70 B3 D5 7E F0 00 42 A4'.replace(' ',''))
app_key = binascii.unhexlify('36 93 92 6E 05 B3 01 A5 02 AB CF CA 43 0D A5 2A'.replace(' ',''))

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)
# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

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

time.sleep(5.0)

#Inicializa OneWire (Comporbar Pin)
onewire = OneWire(Pin('P10'))
#Inicializa Sensor de Temperatura (DS18X20)
tempSensor=DS18X20(onewire)
temperatura_raw = 0
temperatura = 0
while True:
    
    time.sleep(2)
    s.send()
    time.sleep(4)
    rx = s.recv(256)
    if rx:
        print(rx)
    time.sleep(6)
