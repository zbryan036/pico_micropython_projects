#########################################
########### SIMPLE WEB SERVER ###########
#########################################

# hosts a one-page http server with buttons to turn the Pico's LED on or off

###### PHASE 1: POWER ON & IMPORTS ######
from machine import Pin
import time
import rp2
import network
# import urequests as requests
import socket
import sys
from pico_wifi_credentials import netlist

# wifi_credentials.py should be placed in the same folder as this file,
# and should contain a list of networks in the following format:

#netlist = [
    #{'ssid': 'MyWifiNetwork', 'pw': 'MyPassword'},
    #{'ssid': 'MyWifiNetwork_5G', 'pw': 'MyOtherPassword'}
    #]


led = Pin('LED', Pin.OUT)

def blink(blinks, repeat=False):
    cycles = 1
    if repeat:
        cycles = 5
    for i in range(cycles):
        for i in range(blinks):
            led.on()
            time.sleep(0.1)
            led.off()
            time.sleep(0.2)
        time.sleep(1.3)

blink(1)

###### PHASE 2: CONNECT TO WI-FI ######
# activate WLAN interface
try:
    rp2.country('US')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
except:
    blink(1, True)
    sys.exit()

# connect to a network
connected = False
current_net = 0

while not connected and current_net < len(netlist):
    # set ssid and pw
    ssid = netlist[current_net]['ssid']
    pw = netlist[current_net]['pw']
    
    # connect
    wlan.connect(ssid, pw)
    
    # wait for connection
    timeout = 10
    while timeout > 0:
        if wlan.status() < 0 or wlan.status() > 3:
            connected = False
            break
        if wlan.status() == 3:
            connected = True
            led.off()
            time.sleep(0.5)
            break
        timeout -= 1
        time.sleep(1)
    
    # authentication failed; try again
    led.on()
    current_net += 1

if connected:
    blink(2)
    print(wlan.ifconfig()[0])
else:
    blink(1, True)
    sys.exit()

###### PHASE 3: LISTEN FOR CONNECTION ######
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
    
except:
    blink(2, True)
    sys.exit()

blink(3)

# handle button clicks
while True:
    try:
        cl, addr = s.accept()
        print()
        print('client connected from ', addr)
        r = cl.recv(1024)
        r = str(r)
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
    except:
        cl.close()
        sys.exit()
