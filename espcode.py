import camera
import urequests as requests
import network
from time import sleep
from machine import Pin

relay1 = Pin(12,Pin.OUT)
relay2 = Pin(13,Pin.OUT)
relay3 = Pin(15,Pin.OUT)
flash = Pin(4,Pin.OUT)

relays = [relay1,relay2,relay3]

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        wlan.connect(ssid, password)
        sleep(1)
        if wlan.isconnected() == True:
            camera.init(0, format=camera.JPEG)
    return True
def check():
    response = requests.get("http://192.168.243.183:5000/")
    print(response.text)
    
    
    
def triggerRelay(index):
    index = index - 1
    relays[index].on()
    sleep(2)
    relays[index].off
    
def upload_image():
    
    camera.init(0, format=camera.JPEG) if not camera.capture() else None
    #flash.on()
    img = camera.capture()
    #flash.off()
    #print(img)
    api_url = "http://192.168.243.183:5000/upload"
    headers = {'Content-Type': 'image/jpeg'}
    camera.deinit()
    while True:
        try:
            response = requests.post(api_url, headers=headers, data=img)
            if response.status_code == 200:
                print('OK')
                print(response.text)
                if response.text == 'elephant':
                    triggerRelay(1)
                elif response.text == 'bear':
                    triggerRelay(2)
                elif response.text == 'zebra':
                    triggerRelay(3)
                return
            else:
                print(response.status_code)
                print("Failed to upload image. Retrying...")
                sleep(1)
        except Exception as e:
            if e == '-202':
                print("API Inaccessible")
            else:
                print(e)
                print("Retrying...")
                sleep(1)

                
                
                
                
                

def main():
    ssid = "Bala"
    password = "12345678"
    
    while not connect_wifi(ssid, password):
        print("Failed to connect to WiFi. Retrying...")
        sleep(5)

    while True:
        #check()
        
        upload_image()
        sleep(2)

if __name__ == "__main__":
    main()

