######## USAGE ########
# from machine import Pin
# from time import sleep
# import rp2
# import network
# import CONNECT

# netlist = [('ssid', 'password'), ('ssid', 'password'), ... ]
# CONNECT.connect(netlist, rp2, network, sleep, Pin)

def connect(netlist, rp2, network, sleep, Pin):
    rp2.country('US')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    connected = False
    current_net = 0
    led = Pin('LED', Pin.OUT)

    # attempt a connection for each network in the list
    while not connected and current_net < len(netlist):
        ssid = netlist[current_net][0]
        pw = netlist[current_net][1]
        print('attempting connection to', ssid)
        wlan.connect(ssid, pw)
        connected = False
        # wait for connection
        for timeout in range(32, 0, -1):
            print(str(timeout) + '...', end='')
            print(wlan.status())
            if wlan.status() == 3:
                connected = True
                break
            if wlan.status() == -2:
                print('hmmmm... It appears the specified network does not exist')
                break
            if wlan.status() < 0 or wlan.status() > 3:
                raise ValueError('Connection to %s has an invalid status code: %d' % (ssid, wlan.status()))
            sleep(0.5)
            # toggle LED while waiting
            if timeout % 2 == 0:
                led.on()
            else:
                led.off()
        print()
        current_net += 1
    led.off()
    if not connected:
        raise ValueError('None of the ssid/password combos in netlist resulted in a successful login')
    # return IP address
    return wlan
