#Gestion de los sensores
#JUAN MANUEL GALÁN SERRANO
#ALSTOM-UPC 2017
#==============================================================================#
from machine import Timer
from machine import SD
from network import LoRa
from pysense import Pysense
from LuzSensor import LuzSensor
from PresionSensor import PresionSensor
from HumedadSensor import HumedadSensor
import machine
import ubinascii
import builtins
import os

class Gestion:
    """
        Clase encargada de gestionar todos los sensores de la placa Pysense.
    """
    acc = None

    def __init__(self,sd=0):
        self.py = Pysense()
        self.ambientLight = LuzSensor(pysense = self.py);
        self.pressure = PresionSensor(pysense = self.py);
        self.tempHum = HumedadSensor(pysense = self.py);
        self.mininterval = 0
        self.sd = sd
        if self.sd is 1:
            sd = SD()
            os.mount(sd, '/sd')
            os.listdir('/sd')
    def crearjson(self):
        """
            Rellena un tupple con las lecturas de todos los sensores que han sido
            leídos desde la última publicación.
        """
        tup = (0,0,0,0)
        """ Se comprueba la propiedad update de cada sensor por separado y se va
            sumando al tupple
        """
        if self.ambientLight.update is 1:
            tup[0] = self.ambientLight.raw[0]
            print('Añadido valor luminosidad a tup')
            self.ambientLight.update = 0
        if self.pressure.update is 1:
            tup[1] = self.pressure.raw
            print('Añadido valor presion a tup')
            self.pressure.update = 0
        if self.tempHum.update is 1:
            tup[2] = self.tempHum.raw
            print('Añadido valor humedad a tup')
            self.tempHum.update = 0
        tup[3] = self.py.read_battery_voltage()
        print('Añadido valor batería a tup')
        """ Se crea el objeto JSON. Si hay error en la convesión se imprime
            por pantalla y devuelve un 0.
        """
        print('Tupple valores de sensores:' + tup)
        return (tup)
        if self.sd is 1:
            guardarEnSD(buf);
    def intervaloMinimo(self):
        """ Cálculo del intervalo mínimo en la toma de medidas. Este intervalo
            mínimo se usará como intervalo de publicación de los datos vía LoRA.
        """
        self.mininterval = min(self.ambientLight.interval,self.pressure.interval,self.tempHum.interval)
        return self.mininterval
    def modificarIntervalo(self,intervalo,sensor=''):
        """ Función para modificar el intervalo de un sensor. Sus argumentos son:
                intervalo: Número de segundos. Período de toma de datos del sensor.
                            Antes de la llamada a esta función el intervalo por
                            defecto es 20 segundos.
                sensor: Inicial del sensor al que le será modificada la
                        variable intervalo. Si no es correcto, se imprimirá un
                        mensaje por pantalla y ningún intervalo será modificado.
        """
        if sensor is 'L':
            self.ambientLight.interval = intervalo
            self.ambientLight.activarPub()
            print("Intervalo Sensor Luminosidad modificado a %d segundos" %self.ambientLight.interval)
        elif sensor is 'P':
            self.pressure.interval = intervalo
            self.pressure.activarPub()
            print("Intervalo Sensor Presion modificado a %d segundos" %self.pressure.interval)
        elif sensor is 'H':
            self.tempHum.interval = intervalo
            self.tempHum.activarPub()
            print("Intervalo Sensor Humedad modificado a %d segundos" %self.tempHum.interval)
        elif sensor is 'A':
            print('¡¡Acelerómetro no listo!!')
        else:
            print("¡¡Valor de Sensor no válido!!")
    def activarSensor(self,sensor='',en=0):
        """ Activa y desactiva la toma de datos de un sensor. Toma los siguientes
            argumentos:
                sensor: Inicial del sensor a activar/desactivar.Si no es correcto,
                se imprimirá un mensaje por pantalla y nada será modificado.
                en: 0/1 Activar/desactivar toma de medidas.
        """
        if sensor is 'L':
            if en is 0:
                self.ambientLight.desactPub()
            else:
                self.ambientLight.activarPub()
        elif sensor is 'P':
            if en is 0:
                self.pressure.desactPub()
            else:
                self.pressure.activarPub()
        elif sensor is 'H':
            if en is 0:
                self.tempHum.desactPub()
            else:
                self.tempHum.activarPub()
        elif sensor is 'A':
            print('Acelerómetro no listo')
        else:
            print("Valor de Sensor no válido")
    def guardarEnSD(self,buf):
            f = open('sd/data.txt', 'w')
            f.write(buf)
            f.close()
