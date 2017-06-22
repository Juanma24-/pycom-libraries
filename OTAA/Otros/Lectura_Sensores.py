from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2
from datosSensor import Lectura

py = Pysense()
pressure = MPL3115A2(py)
tempHum = SI7006A20(py)
ambientLight = LTR329ALS01(py)
acc = LIS2HH12(py)
prueba = datosSensor()
#Lectura Voltage batería (mV)
bat = py.read_battery_voltage()
#Lectura lux (Es un vector de 2 componentes)
#TODO: ¿Unidades?¿Significado del vector? Leer Datasheet. (Encontrar en pycom doc)
lux = ambientLight.lux()
#Lectura Humedad
#TODO:¿Unidades? Leer Datasheet (Encontrar en pycom doc)
hum = tempHum.humidity()
#Lectura Temperatura desde Sensor Humedad
#TODO: ¿Unidades? Leer Datasheet (Encontrar en pycom doc)
temph = tempHum.temp()
#Lectura Presión
#TODO: ¿Unidades? Leer Datasheet
press = pressure.alt()
print(lux)
