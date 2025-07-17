# Формуємо гармонічні сигнали за допомогою ШІМ 
# DTMF - через об'єднання гармонік з двох різних виходів через резистори
 
import math
import machine
import time
import _thread

# Parameters
pin_1 = 1      # GPIO pin for PWM output
pin_2 = 2
freq = 12000      # PWM frequency in Hz
sine_freq_1 = 941  # Output sine frequency in Hz
sine_freq_2 = 1633
duration = 0.2   # Duration of the sine wave in sec

# Generate sine table (duty from 0 to 1023 for 10-bit PWM)
samples_1 = []
for i in range(int(freq * duration)):
    t = i / freq
    # normalize to [0, 65535]
    val = math.sin(2 * math.pi * sine_freq_1 * t)
    duty = int((val / 2 + 0.5) * 65535)
    samples_1.append(duty)

samples_2 = []
for i in range(int(freq * duration)):
    t = i / freq
    # normalize to [0, 65535]
    val = math.sin(2 * math.pi * sine_freq_2 * t)
    duty = int((val / 2 + 0.5) * 65535)
    samples_2.append(duty)


# Set up PWM
pwm_1 = machine.PWM(machine.Pin(pin_1))
pwm_1.freq(freq)

pwm_2 = machine.PWM(machine.Pin(pin_2))
pwm_2.freq(freq)


def gen_tone():
    while True:
        for duty in samples_1:
            pwm_1.duty_u16(duty)
            #time.sleep_us(int(1e6 / (freq*1.8))) # приблизна залежність
            time.sleep_us(64) # підбираємо затримку! залежить від freq
        pwm_1.duty_u16(0)    

def gen_tone_2(samples):
    for duty in samples:
        pwm_2.duty_u16(duty)
        #time.sleep_us(int(1e6 / (freq*1.8)))
        time.sleep_us(65)  # підбираємо затримку! залежить від freq
    pwm_2.duty_u16(0)

_thread.start_new_thread(gen_tone, ())


while True:
    gen_tone_2(samples_2)

        