from machine import Pin
from machine import Timer
import time

duration = 80 # duration in ms

pin_1 = Pin(1, Pin.OUT)
pin_2 = Pin(2, Pin.OUT)

# на управління реле ("0" - викл. живлення тлф. для подачі DTMF)
pin_en = machine.Pin(16, machine.Pin.OUT)
pin_en.value(1)

# DTMF frequencies 
DTMF_FREQS = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
    }

tim_1 = Timer() # freq low
tim_2 = Timer() # freq hi
tim_duration = Timer() # duration DTMF

def callback_1(t):
    if en_dtmf:
        pin_1.toggle()
    
def callback_2(t):
    if en_dtmf:
        pin_2.toggle()    

def callback_duration(t):
    global en_dtmf
    en_dtmf = False


def dial_num(sequence):
    global en_dtmf
    pin_en.value(0)
    for symbol in sequence:
        if symbol in DTMF_FREQS:
            freq_low, freq_hi = DTMF_FREQS[symbol]
        else:
            print('Невірний символ у послідовності!')
            continue
        en_dtmf = True            
        tim_duration.init(mode=Timer.ONE_SHOT,
                          period=duration,
                          callback=callback_duration)
        tim_1.init(mode=Timer.PERIODIC,
                   freq=freq_low*2,
                   callback=callback_1)
        tim_2.init(mode=Timer.PERIODIC,
                   freq=freq_hi*2,
                   callback=callback_2)
        while en_dtmf:
            pass
        time.sleep_ms(200)
    pin_en.value(1)
        
# послідовність для зміни рівнів тлф та мкф: *00#058#AA*BB#
# AA - speaker volume in range 00-99
# BB - mic volume in range 00-15

en_dtmf = False
while True:
    sequence = input('Введіть номер: ')
    dial_num(sequence)
