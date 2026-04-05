from machine import Pin, PWM
import time
import network
import socket

class Wheel:
    def __init__(self):
        self.stby = Pin(26, Pin.OUT)
        self.stby.value(1)

        self.ain1 = Pin(27, Pin.OUT)
        self.ain2 = Pin(12, Pin.OUT)
        self.pwma = PWM(Pin(33))
        self.pwma.freq(1000)

        self.bin1 = Pin(14, Pin.OUT)
        self.bin2 = Pin(13, Pin.OUT)
        self.pwmb = PWM(Pin(25))
        self.pwmb.freq(1000)
        
        self.stop() # Start pe car stop rahegi
        
        self.state = "S"

    def set_speed(self, speed=350): # Thoda zyada speed rakhte hain (0-1023)
        self.pwma.duty(speed)
        self.pwmb.duty(speed)

    def move_backward(self):
        self.ain1.value(1)
        self.ain2.value(0)
        self.bin1.value(0)
        self.bin2.value(1)
        self.state = "B"

    def move_forward(self):
        self.ain1.value(0)
        self.ain2.value(1)
        self.bin1.value(1)
        self.bin2.value(0)
        self.state = "F"

    def stop(self):
        self.ain1.value(0)
        self.ain2.value(0)
        self.bin1.value(0)
        self.bin2.value(0)
        self.set_speed(0)
        self.state = "S"
        
    def move_right_forward(self):
        self.ain1.value(0)
        self.ain2.value(0)
        self.bin1.value(1)
        self.bin2.value(0)
    
    def move_left_forward(self):
        self.ain1.value(0)
        self.ain2.value(1)
        self.bin1.value(0)
        self.bin2.value(0)
    
    def move_right_backward(self):
        self.ain1.value(0)
        self.ain2.value(0)
        self.bin1.value(0)
        self.bin2.value(1)
    
    def move_left_backward(self):
        self.ain1.value(1)
        self.ain2.value(0)
        self.bin1.value(0)
        self.bin2.value(0)
    
    def get_state(self):
        return self.state

# --- Wi-Fi Setup ---
# AP - Access Point - Where ESP32 creates its own wifi network
# SP - Station - Where ESP32 connects to existing wifi network
ap = network.WLAN(network.AP_IF)
# Config wifi name and password
ap.config(essid='Trahymam', password='Trahymam')
# start sending signals
ap.active(True)

print("Wi-Fi Active: Connect to 'Trahymam'")
print("IP:", ap.ifconfig()[0])

# --- UDP Socket Setup ---
# IP - Like home address of ESP32
UDP_IP = "192.168.4.1"
# Port - like room number, where we will receive data from OpenCV
UDP_PORT = 5005

# Once wifi connected, socket helps to receive data from OpenCV
# UDP - User Datagram Protocol, simple way to send data without any handshakes, faster than TCP(Transmission Control Protocol)
# AF_INET - Address Family Internet, means we are using IP address
# SOCK_DGRAM - Socket Type Datagram, means we are using UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the IP and Port, so that it can listen for incoming data on that address
sock.bind((UDP_IP, UDP_PORT))

# Initialize Wheel class once
wheel = Wheel()

print("Waiting for OpenCV commands...")

last_status = ""
while True:
    try:

        # Non-blocking read (optional) ya simple receive
        # It can listen upto 1024 bytes of data
        data, addr = sock.recvfrom(1024)
        # Decode the bytes into string and strip removes extra spaces
        command = data.decode().strip()
        
        print("Command Received:", command)
        
        # Set Direction
        if command == "F":
            wheel.set_speed(500) # Speed adjust kar sakte hain
            wheel.move_forward()
        elif command == "B":
            wheel.set_speed(500)
            wheel.move_backward()
        elif command == "S":
            wheel.stop()
        elif command == "L":
            if wheel.get_state() == "F":
                wheel.set_speed(350)
                wheel.move_left_forward()
            elif wheel.get_state() == "B":
                wheel.set_speed(350)
                wheel.move_left_backward()
        elif command == "R":
            if wheel.get_state() == "F":
                wheel.set_speed(350)
                wheel.move_right_forward()
            elif wheel.get_state() == "B":
                wheel.set_speed(350)
                wheel.move_right_backward()
            wheel.set_speed(350)
            wheel.steer_right()
        
        # Set Speed
        if command == "1":
            wheel.set_speed(350) 
        elif command == "2":
            wheel.set_speed(700)
        elif command == "3":
            wheel.set_speed(1000)
        
        last_status = command
    except Exception as e:
        print("Error:", e)
        time.sleep(0.1)

