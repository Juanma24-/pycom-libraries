from machine import Timer

class Clock:
    def __init__(self):
        self.seconds = 0
        self.__alarm = Timer.Alarm(self._seconds_handler,1,periodic=True)
    def _seconds_handler(self, alarm):
        self.seconds += 1
        print("%02d seconds hav passed" %self.seconds)
        if self.seconds == 10:
            alarm.cancel()
clock= Clock()
