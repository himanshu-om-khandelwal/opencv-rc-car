import socket
import cv2

# ESP32 ki Details
UDP_IP = "192.168.4.1"
UDP_PORT = 5005

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_esp32(message):
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

# Camera start karein
cap = cv2.VideoCapture(0)

print("Control start! F: Forward, S: Stop, Q: Quit")

while True:
    ret, frame = cap.read()
    if not ret: break

    cv2.imshow('Robot Control', frame)
    
    key = cv2.waitKeyEx(1) 
    if key == -1: continue  # No key pressed, continue loop
    print(f'key: {key}')
    # Set Directions
    if key == 82 or key == 2490368:
        send_to_esp32("F")
        print("Moving Forward")
    elif key == 84 or key == 2621440:
        send_to_esp32("B")
        print("Moving backward")
    elif key == 81 or key == 2424832:
        send_to_esp32("L")
        print("Steering Left")
    elif key == 83 or key == 2555904:
        send_to_esp32("R")
        print("Steering Right")
    
    char_key = key & 0xFF
    print(f'char_key: {char_key}')
    # Set Speed
    if char_key == ord('q'):
        break
    elif char_key == ord('s'):
        send_to_esp32("S")
        print("Stop")
    elif char_key == 49:
        send_to_esp32("1")
        print("Speed: 250")
    elif char_key == 50:
        send_to_esp32("2")
        print("Speed: 500")
    elif char_key == 51:
        send_to_esp32("3")
        print("Speed: 750")
    elif char_key == 52:
        send_to_esp32("4")
        print("Speed: 1000")

cap.release()
cv2.destroyAllWindows()