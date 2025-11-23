from machine import Timer,Pin

led = Pin("LED", mode = Pin.OUT)
def callback5000(n):
    led.on()
    time
    else:
        led.off()
        
def main():
    
    timer = Timer(period=2000, callback=callback2000)
    
if __name__ == "__main__":

    main()