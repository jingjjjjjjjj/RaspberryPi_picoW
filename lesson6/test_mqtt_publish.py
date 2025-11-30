#!/usr/bin/env python3
"""
Test MQTT Publisher
持續發佈測試感測器數據到 MQTT broker
"""
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "客廳/感測器"

# 基礎溫度和濕度值
BASE_TEMP = 25.0
BASE_HUMIDITY = 60.0

def on_connect(client, userdata, flags, rc, properties=None):
    """連線回調"""
    if rc == 0:
        print(f"✓ 已連接至 MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"✗ 連接失敗，代碼: {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    """斷開連線回調"""
    if rc != 0:
        print(f"✗ 非預期斷開連線，代碼: {rc}")
    else:
        print("✓ 已斷開連線")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """發佈回調（相容 v1 和 v2 API）"""
    # 可選：顯示發佈確認
    pass

def generate_sensor_data():
    """生成感測器數據"""
    # 溫度：±2°C 波動
    temperature = BASE_TEMP + random.uniform(-2, 2)
    
    # 濕度：±5% 波動
    humidity = BASE_HUMIDITY + random.uniform(-5, 5)
    humidity = max(0, min(100, humidity))  # 限制在 0-100%
    
    # 光照狀態：隨機開/關
    light_status = random.choice([True, False])
    
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "light_status": light_status
    }

def main():
    """主函數"""
    # 根據 paho-mqtt 版本自動選擇 Callback API
    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id="test_publisher"
        )
    except (AttributeError, TypeError):
        # 舊版本的 paho-mqtt（< 2.0）
        client = mqtt.Client(client_id="test_publisher")
    
    # 設定回調
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    try:
        # 連接到 broker
        print(f"正在連接至 {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # 啟動網路循環（非阻塞）
        client.loop_start()
        
        # 給連接時間建立
        time.sleep(1)
        
        print(f"\n開始發佈測試數據至主題: {MQTT_TOPIC}")
        print("按 Ctrl+C 停止\n")
        
        # 每 3 秒發佈一次數據
        counter = 0
        while True:
            data = generate_sensor_data()
            
            # 發佈 JSON 數據
            payload = json.dumps(data, ensure_ascii=False)
            result = client.publish(MQTT_TOPIC, payload, qos=1)
            
            # 顯示發佈結果
            status_str = "✓" if result.rc == mqtt.MQTT_ERR_SUCCESS else "✗"
            counter += 1
            print(f"[{counter}] {status_str} 發佈: 溫度={data['temperature']}°C, "
                  f"濕度={data['humidity']}%, 光照={'開' if data['light_status'] else '關'}")
            
            # 等待 3 秒後發佈下一筆數據
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n已停止發佈")
    except Exception as e:
        print(f"\n✗ 錯誤: {e}")
    finally:
        # 清理資源
        client.loop_stop()
        client.disconnect()
        print("已清理資源並斷開連線")

if __name__ == "__main__":
    main()
