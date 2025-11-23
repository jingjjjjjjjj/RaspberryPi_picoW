from machine import Timer,Pin
import time

#全域變數，避免每次callback都要創建新的Pin物件
led = Pin("LED", mode = Pin.OUT)

def callback5000(n):
    for i in range (2):
        led.on()
        time.sleep_ms(100)
        led.off()
        if i < 1:
            time.sleep_ms(100)

        
def main():
    timer = Timer(period=5000, callback=callback5000)
    
if __name__ == "__main__":
    main()