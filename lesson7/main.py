import wifi_connect
import time

wifi_connect.connect()

print("IP:",wifi_connect.get_ip())

while True:
    print("-"*30)
    if wifi_connect.test_internet():
        print("外部網路OK")
    else:
        print("外部網路無法連線")
    print("等待10秒後再測試...")
    time.sleep(10)