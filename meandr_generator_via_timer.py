# Формування неперервних меандр-імпульсів через таймери
# Може бути використано для генерації DTMF сигналів (перша гармонік меандра),
# якщо об'єднати (наприклад через резистори) два сигнали
from machine import Pin
from machine import Timer


# example, DTMF '4': f_low=770Hz, f_hi=1209Hz
freq_low = 770
freq_hi = 1209

pin_1 = Pin(1, Pin.OUT)
pin_2 = Pin(2, Pin.OUT)

def callback_1(t):
    pin_1.toggle()

def callback_2(t):
    pin_2.toggle()

tim_1 = Timer() # freq low
tim_2 = Timer() # freq hi

tim_1.init(mode=Timer.PERIODIC,
           freq=freq_low*2,
           callback=callback_1)

tim_2.init(mode=Timer.PERIODIC,
           freq=freq_hi*2,
           callback=callback_2)

while True:
    pass
