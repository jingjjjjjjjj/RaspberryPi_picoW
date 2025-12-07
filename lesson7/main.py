import wifi_connect

wifi_connect.connect()

print("IP:",wifi_connect.get_ip())

if wifi_connect.test_internet():
    print("外部網路OK")
else:
    print("外部網路無法連線")