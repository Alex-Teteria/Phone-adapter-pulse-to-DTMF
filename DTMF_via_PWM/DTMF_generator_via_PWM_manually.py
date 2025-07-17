# Формуємо DTMF через об'єднання гармонік з двох різних виходів через резистори
# -----------------------------------------------------------------------------
# Author: Alex Teteria
# v0.2
# 11.07.2025
# Implemented and tested on Pi Pico with RP2040
# Released under the MIT license
 
import machine
import time
import _thread
import json


# Parameters
pin_1 = 1    # GPIO pin for PWM output 1
pin_2 = 2    # GPIO pin for PWM output 2  
freq = 12000 # PWM frequency in Hz

# на управління реле ("0" - викл. живлення тлф. для подачі DTMF)
pin_en = machine.Pin(16, machine.Pin.OUT)
pin_en.value(1)

# сформовані раніше та записані у файли послідовності
# для нижніх та верхніх частот DTMF
filename_low = "DTMF_low_dict.json"
filename_hi = "DTMF_hi_dict.json"

# DTMF frequencies 
DTMF_FREQS = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
    }

# set up PWM for low freq
pwm_1 = machine.PWM(machine.Pin(pin_1))
pwm_1.freq(freq)
# set up PWM for hi freq
pwm_2 = machine.PWM(machine.Pin(pin_2))
pwm_2.freq(freq)


def gen_tone():
    global tone_1
    while True:
        try:
            if tone_1:
                time.sleep_ms(200)
                for duty in samples_1:
                    pwm_1.duty_u16(duty)
                    time.sleep_us(65) # підбираємо затримку! залежить від PWM frequency
                pwm_1.duty_u16(0)
        except:
            continue


with open(filename_low, 'r', encoding='utf-8') as f:
        data_low = json.load(f)
        
with open(filename_hi, 'r', encoding='utf-8') as f:
        data_hi = json.load(f)

def get_samples(name_sequence):
    if name_sequence in DTMF_FREQS:
        f_low, f_hi = DTMF_FREQS[name_sequence]
        samples_1 = data_low[str(f_low)]
        samples_2 = data_hi[str(f_hi)]
        return samples_1, samples_2
    else:
        print('Номер невірний')


def gen_tone_2(samples):
    for duty in samples:
        pwm_2.duty_u16(duty)
        time.sleep_us(65)  # підбираємо затримку! залежить від PWM frequency
    pwm_2.duty_u16(0)


def dial_num(sequence):
    global samples_1, samples_2, tone_1
    pin_en.value(0)
    for symbol in sequence:
        try:
            samples_1, samples_2 = get_samples(symbol)
        except:
            print('Невірний символ у послідовності!')
        tone_1 = True
        time.sleep_ms(200)
        gen_tone_2(samples_2)
        tone_1 = False
    pin_en.value(1)
   

samples_1 = []
tone_1 = False
_thread.start_new_thread(gen_tone, ())

in_1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    sequence = input('Введіть номер: ')
    dial_num(sequence)
    
    
    
