#Librería Sensor de Presion
#JUAN MANUEL GALÁN SERRANO
#ALSTOM-UPC 2017
#=========================
from machine import Timer
from pysense import Pysense
from SI7006A20 import SI7006A20
class HumedadSensor:
    """
        Funciones de control del sensor de Humedad SI7006A20.
    """
    tempHum = None

    def __init__(self, pysense=None):
        if pysense is None:
            self.pysense = Pysense()
        self.last = 0
        self.raw = 0
        self.magic = 'LoPy'
        self.update = 0
        self.interval = 20
        HumedadSensor.tempHum = SI7006A20(pysense)
        if (HumedadSensor.tempHum is not None):
            print('Cargado Sensor Humedad con éxito')
            self.alarmh = Timer.Alarm(self.leerhumedad, self.interval, periodic=True)
    def leerhumedad(self,alarmh):
        self.raw = HumedadSensor.tempHum.humidity()
        self._compare_update()
        print("Humedad: %f" %self.raw)
    def _compare_update(self):
        if self.raw is not self.last :
            self.last = self.raw
            self.update = 1
        else:
            self.update = 0
    def desactPub(self):
        self.alarmh.cancel()
        print("Desactivada publicación Sensor Humedad")
    def activarPub(self):
        self.alarmh.cancel()
        self.alarmh = Timer.Alarm(self.leerhumedad, self.interval, periodic=True)
        print("Activada publicación Sensor Humedad")
