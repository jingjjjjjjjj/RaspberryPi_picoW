from machine import Pin
from time import sleep

btn_pin = 14
led_pin = 15

led = Pin(led_pin, Pin.OUT)
button = Pin(btn_pin, Pin.IN, Pin.PULL_UP)


while (True):
    if button.value() == 1:
        print("XXX")
        led.off()
    else:
        print("OOO")
        led.on()
        sleep(1)