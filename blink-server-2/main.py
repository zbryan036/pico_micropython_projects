######## Blink Server 2 ########
# Cycles through a list of WiFi networks, trying to connect. If the
# connection is successful, blinks out its IP address and serves a
# simple web page allowing users on the network to turn the LED on or
# off

from machine import Pin
from time import sleep
import rp2
import network
import socket

# custom modules
import pico_connect
import pico_signal
from pico_wifi_credentials import netlist

ip = None

try:
    wlan = pico_connect.connect(netlist, rp2, network, sleep, Pin)
    ip = wlan.ifconfig()[0]
    pico_signal.success(Pin, sleep)
    pico_signal.address(Pin, sleep, ip, 1)
except Exception as e:
    pico_signal.fail(Pin, sleep, e)
    raise ValueError(e)

# listen for http connection on port 80
try:
    def get_html(html_name):
        with open(html_name, 'r') as file:
            html = file.read()
        return html

    addr = socket.getaddrinfo(wlan.ifconfig()[0], 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('listening on ', addr)
    pico_signal.success(Pin, sleep)
except Exception as e:
    pico_signal.fail(Pin, sleep, e)
    raise ValueError(e)

# handle button clicks
while True:
    try:
        cl, addr = s.accept()
        print('client connected from ', addr)
        r = cl.recv(1024)
        r = str(r)
        led = Pin('LED', Pin.OUT)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')
        if led_on == 7:
            led.on()
        if led_off == 7:
            led.off()
        
        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except Exception as e:
        pico_signal.fail(Pin, sleep, e)
        raise ValueError(e)
