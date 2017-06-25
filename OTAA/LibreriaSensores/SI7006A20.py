import time

class SI7006A20:

    SI7006A20_I2C_ADDR = const(0x40)
    TEMP_NOHOLDMASTER = const(0xF3)
    HUMD_NOHOLDMASTER = const(0xF5)

    def __init__(self, pysense=None, sda='P22', scl='P21'):
        if pysense is not None:
            self.i2c = pysense.i2c
        else:
            from machine import I2C
            self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl))

    def _concat_hex(self, a, b):
        sizeof_b = 0
        while((b >> sizeof_b) > 0):
            sizeof_b += 1
        sizeof_b += sizeof_b % 8
        return (a << sizeof_b) | b

    def temp(self, unit=None):
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0xF3]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR,2)
        data0 = data[0]
        data1 = data[1]
        #Palabra de 16 bits según Datasheet
        data = (data1<<8|data0)
        #data = self._concat_hex(data0, data1)
        #Se puede sustituir la division por >>16
        #temp = ((175.72 * data) / 65536.0) - 46.85
        temp = ((175.72 * data) >> 16) - 46.85
        if unit == 'F':
            temp = temp * 1.8 + 32
        return temp

    def humidity(self):
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0xF5]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR,2)
        data0 = data[0]
        data1 = data[1]
        # Es una palabra de 16 bits según Datasheet
        data = data1<<8|data0
        #data = self._concat_hex(data0, data1)
        #Se puede sustituir la division por >>16
        humidity = ((125.0 * data) >> 16) - 6.0
        #humidity = ((125.0 * data) / 65536.0) - 6.0
        return humidity
