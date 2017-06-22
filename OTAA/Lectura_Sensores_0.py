#JUAN MANUEL GALÁN SERRANO
#ALSTOM-UPC 2017
#==============================================================================#
# Archivo de prueba para comprobar el correcto funcionamiento de la clase de
# gestión de los sensores y los sensores en sí.
#==============================================================================#
from pysense import Pysense
from GestionSensores import Gestion
from machine import Timer
import binascii
import time
import machine
#------------------------------------------------------------------------------#
# Función encargada de crear la cadena en formato JSON con los datos de los
# sensores medidos.
def publicarJSON(alarmaPub):
        print("Creando JSON")
        json = gestion.crearjson()
#------------------------------------------------------------------------------#
# Código de las pruebas.
#Crea una instancia para gestionar los sensores.
gestion = Gestion()
time.sleep(4)
# Se busca en intervalo mínimo de lectura de datos en los sensores.
intervalopub = gestion.intervaloMinimo()
print("Intervalo de Publicacion: %d segundos"  %(intervalopub))
# Fija el intervalo creación de JSON como el mínimo de los intervalos de lectura.
alarmaPub = Timer.Alarm(publicarJSON, intervalopub, periodic=True)
time.sleep(60)
# Fija el intervalo del sensor de Luminosidad en 30s (por defecto 20s)
gestion.modificarIntervalo(30,'L')
time.sleep(120)
# Desactiva todos los sensores
gestion.activarSensor(sensor='L',en=0)
gestion.activarSensor(sensor='P',en=0)
gestion.activarSensor(sensor='H',en=0)
alarmaPub.cancel()
time.sleep(120)
# Vuelve a activar todos los sensores
gestion.activarSensor(sensor='L',en=1)
gestion.activarSensor(sensor='P',en=1)
gestion.activarSensor(sensor='H',en=1)
intervalopub = gestion.intervaloMinimo()
alarmaPub = Timer.Alarm(publicarJSON, intervalopub, periodic=True)

# FIN PROGRAMA
