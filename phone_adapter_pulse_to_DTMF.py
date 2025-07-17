# Author: Alex Teteria
# v0.2
# 11.07.2025
# Implemented and tested on Pi Pico with RP2040
# Released under the MIT license

from machine import Pin
from machine import Timer
import time
from measuring_time_intervals import Pulse_measure
import _thread
import json


duration = 60 # duration DTMF in ms

pin_1 = Pin(1, Pin.OUT)
pin_2 = Pin(2, Pin.OUT)

# на управління реле ("0" - викл. живлення тлф. для подачі DTMF)
pin_en = machine.Pin(16, machine.Pin.OUT)
pin_en.value(1)

# файл телефонний довідник
# формат файла: {'NN': 'NNNNNNNNN'}
# ключ словника - короткий номер із двох цифр,
# дані - 9 цифр дійсного номера (без першого "0", який набирається автоматично)
filename = "phone_directory.json" # файл телефонний довідник
# номер голосового меню,
# буде набрано за умови відсутності набраного номера в довіднику
voice_menu = '800205433'

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

# вхід з імпульсного номеронаберача
in_1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
imp = Pulse_measure(in_1)

def callback_1(t):
    'low freq DTMF'
    if en_dtmf:
        pin_1.toggle()
    
def callback_2(t):
    'hi freq DTMF'
    if en_dtmf:
        pin_2.toggle()    

def callback_duration(t):
    'stop DTMF'
    global en_dtmf
    en_dtmf = False


def dial_num(sequence):
    if sequence is None:
        return
    global en_dtmf
    pin_en.value(0)
    for symbol in sequence:
        if symbol in DTMF_FREQS:
            freq_low, freq_hi = DTMF_FREQS[symbol]
        else:  # якщо символ не вірний, то пропускаємо його
            print('Невірний символ у послідовності!')
            continue
        en_dtmf = True  # start DTMF          
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

    
def get_sequence():
    global dial_start
    symbol = get_symbol()
    if symbol == '2' and dial_start:
        return get_short()
    if symbol:
       dial_start = False
    return symbol

def get_short():
    global dial_start
    dial_start = False
    dial_num('0')
    sequence = []
    while len(sequence) != 2:
        time.sleep_ms(60)
        symbol = get_symbol()
        if dial_start:
            return
        if symbol:
            sequence.append(symbol)
    return phone_directory.get(''.join(sequence), voice_menu)    

def end_dial():
    global dial_continue
    dial_continue = False

def get_symbol():
    while not imp.data_en:
        if dial_start:
            return
    num_t = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    if imp.pulse in num_t:
        name = '0' if imp.pulse == 10 else str(imp.pulse)
    else:
        name = None
    return name    

def handset():
    '''якщо слухавку покладено,
       то змінна dial_start = True
    '''
    global dial_start
    while True:
        try:
            if in_1.value(): # слухавка лежить
                for i in range(20):
                    time.sleep_ms(40)
                    if not in_1.value():
                        break
                else:
                    dial_start = True
                if print_en:
                    print('2 потік!', dial_start)
                    print_en = False
            else:
               print_en = True 
        except:
            continue
                            

# послідовність для зміни рівнів тлф та мкф: *00#058#AA*BB#
# AA - speaker volume in range 00-99
# BB - mic volume in range 00-15

with open(filename, 'r', encoding='utf-8') as f:
    phone_directory = json.load(f)
    

en_dtmf = False
dial_start = True

# другий потік: відслідковуємо чи слухавку піднято
_thread.start_new_thread(handset, ())

while True:
    sequence = get_sequence()
    dial_num(sequence)


