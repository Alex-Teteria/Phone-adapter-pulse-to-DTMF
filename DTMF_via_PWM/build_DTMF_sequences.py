import math
# from machine import Pin, PWM
import json


freq = 12000    # PWM frequency in Hz
duration = 0.2  # Duration of the sine wave in sec

filename_low = "DTMF_low_dict.json"
filename_hi = "DTMF_hi_dict.json"

# DTMF frequencies 
DTMF_FREQS = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
}

def gen_samples(sine_freq):
    # Generate sine table (duty from 0 to 1023 for 10-bit PWM)
    samples = []
    for i in range(int(freq * duration)):
        t = i / freq
        # normalize to [0, 65535]
        val = math.sin(2 * math.pi * sine_freq * t)
        duty = int((val / 2 + 0.5) * 65535)
        samples.append(duty)
    return samples

samples_low = {}
samples_hi = {}

for symbol in ('1', '5', '9', 'D'):
    f_low, f_hi = DTMF_FREQS[symbol]
    samples_low[f_low] = gen_samples(f_low)
    samples_hi[f_hi] = gen_samples(f_hi)


with open(filename_low, "w") as f:
    json.dump(samples_low, f)
print(f"Словник записано у файл {filename_low}")

with open(filename_hi, "w") as f:
    json.dump(samples_hi, f)
print(f"Словник записано у файл {filename_hi}")


with open(filename_hi, 'r', encoding='utf-8') as f:
      data = json.load(f)

print(data['1633'][0], type(data['1633'][0]))
      