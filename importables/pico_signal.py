######## USAGE ########
# from machine import Pin
# from time import sleep
# import SIGNAL

# SIGNAL.success(Pin, sleep)
# SIGNAL.fail(Pin, sleep, message='print this to console')
# SIGNAL.address(Pin, sleep, '192.168.0.71')

def success(Pin, sleep):
    print('Success')
    led = Pin('LED', Pin.OUT)
    led.off()
    sleep(0.8)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.12)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.32)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.32)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.12)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.32)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.72)
    led.on()
    sleep(0.08)
    led.off()

def fail(Pin, sleep, message=''):
    print('Fail')
    print(message)
    led = Pin('LED', Pin.OUT)
    led.off()
    sleep(0.8)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.72)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.72)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.72)
    for i in range(16):
        led.on()
        sleep(0.05)
        led.off()
        sleep(0.05)

def blink_ready(led, sleep):
    led.off()
    sleep(2)
    led.on()
    sleep(0.08)
    led.off()
    sleep(0.12)
    led.on()
    sleep(0.08)
    led.off()
    sleep(2)

def blink_digit(led, sleep, digit):
    led.off()
    sleep(0.5)
    if digit == 0:
        led.on()
        sleep(0.5)
        led.off()
        sleep(1)
        return
    for i in range(digit):
        led.on()
        sleep(0.08)
        led.off()
        sleep(0.42)
    sleep(1)

# blinks out the specified ip address one digit at a time
def address(Pin, sleep, ip, iterations=1):
    print('Address:', ip)
    led = Pin('LED', Pin.OUT)
    for i in range(iterations):
        blink_ready(led, sleep)
        for char in ip:
            if char == '.':
                blink_ready(led, sleep)
            else:
                blink_digit(led, sleep, int(char))

