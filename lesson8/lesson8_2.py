from machine import Pin
from time import sleep

btn_pin = 14

button = Pin(btn_pin, Pin.IN, Pin.PULL_UP)
while True:
    print(button.value())
    sleep(1)