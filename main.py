import dht
from machine import Pin, UART
from time import sleep
import utime,time
dht11 = dht.DHT11(Pin(4))

# WIFI 路由器信息，请填上自己的WIFI路由器信息
SSID='Pizza Hut Centro'            # WIFI名称
password = '1223334444'        # WIFI密码
API_KEY ='I3JQEO7ZXHV2PBX0'
ServerIP = 'api.thingspeak.com'   # 电脑端服务器IP地址，需要修改
Port = '80'


# 串口映射到GP0和GP1端口上，在使用该端口和
# WIFI模块通讯时，不要使用GP0和GP1端口
esp_uart = UART(0, 115200) # 串口0,波特率为115200
# 串口映射到GP0和GP1端口上，在使用该端口和

# 发送命令函数
def esp_sendCMD(cmd,ack,timeout=2000):
    esp_uart.write(cmd+'\r\n')
    i_t = utime.ticks_ms()
    while (utime.ticks_ms() - i_t) < timeout:
        s_get = esp_uart.read()
        if(s_get != None):
            s_get=s_get.decode()
            print(s_get)
            if(s_get.find(ack) >= 0):
                return True
    return False




# 程序入口

esp_uart.write('+++')   # 初始化退出透传模式
time.sleep(1)
if(esp_uart.any()>0):
    esp_uart.read()
esp_sendCMD("AT","OK")          # AT指令
esp_sendCMD("AT+CWMODE=3","OK") # 配置 WiFi 模式
esp_sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000) # 连接路由器
esp_sendCMD("AT+CIFSR","OK")     # 查询 WIFI模块的 IP 地址
esp_sendCMD("AT+CIPSTART=\"TCP\",\""+ServerIP+"\","+Port,"OK",10000) # RP2040-w 模块作为 TCP client 连接到服务器
esp_sendCMD("AT+CIPMODE=1","OK")   # 开启透传模式
esp_sendCMD("AT+CIPSEND",">")      # RP2040-w 模块向服务器发送数据



while True:
    dht11.measure()
    t = dht11.temperature()
    h = dht11.humidity()
    sleep(3)

    print('T= ,' , t, '. H=', h)
    sleep(3)

    get_request = "GET /update?api_key={}&field1={}&field2={} HTTP/1.1\r\nHost: api.thingspeak.com\r\n\r\n".format(API_KEY, t+2,h)


    request_length = len(get_request)+5
    print("Request Length including \\r\\n:", request_length)

    #esp_sendCMD("AT+CIPSEND={}".format(request_length), ">")
    
    esp_uart.write(get_request)
    sleep(30)

