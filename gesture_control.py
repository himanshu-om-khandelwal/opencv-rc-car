import mediapipe as mp
import cv2
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import socket

class HandGesture:
    def __init__(self):
        # 1. Variables for tracking state
        self.current_gesture = "S"  # Initial state
        self.last_timestamp = 0
        
        # 2. MediaPipe Task Setup (Live Stream Mode for true Async)
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO, # Asynchronous mode
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.result = None

    def update_gesture(self):
        """Internal callback: Background mein gestures update karne ke liye."""
        if not self.result.hand_landmarks:
            self.current_gesture = "S"
            return

        landmarks = self.result.hand_landmarks[0]

        self.current_gesture = self.process_logic(landmarks)

    def process_logic(self, landmarks):
        print(f'Processing landmarks: {landmarks}')

        wrist_y = landmarks[0].y

        thumb_cmc_y = landmarks[1].y
        thumb_mcp_y = landmarks[2].y
        thumb_ip_x = landmarks[3].x
        thumb_ip_y = landmarks[3].y
        thumb_tip_x = landmarks[4].x
        thumb_tip_y = landmarks[4].y

        index_mcp_y = landmarks[5].y
        index_pip_x = landmarks[6].x
        index_dip_x = landmarks[7].x
        index_tip_x = landmarks[8].x
        index_tip_y = landmarks[8].y
        
        middle_mcp_y = landmarks[9].y
        middle_pip_x = landmarks[10].x
        middle_tip_x = landmarks[12].x
        middle_tip_y = landmarks[12].y

        ring_mcp_y = landmarks[13].y
        ring_pip_x = landmarks[14].x
        ring_tip_x = landmarks[16].x
        ring_tip_y = landmarks[16].y

        pinky_mcp_y = landmarks[17].y
        pinky_pip_x = landmarks[18].x
        pinky_tip_x = landmarks[20].x
        pinky_tip_y = landmarks[20].y

        is_hand_open = index_tip_y < index_mcp_y and middle_tip_y < middle_mcp_y and ring_tip_y < ring_mcp_y and pinky_tip_y < pinky_mcp_y

        is_fist = index_tip_y > index_mcp_y and middle_tip_y > middle_mcp_y and ring_tip_y > ring_mcp_y and pinky_tip_y > pinky_mcp_y

        is_thumb_close = thumb_tip_x >= thumb_ip_x and thumb_tip_x + 0.1 >= index_dip_x

        is_tilted_left = index_mcp_y > middle_mcp_y > ring_mcp_y > pinky_mcp_y

        is_tilted_right = index_mcp_y < middle_mcp_y < ring_mcp_y < pinky_mcp_y

        print(f'''
              is_hand_open: {is_hand_open},
              is_fist: {is_fist},
              is_thumb_close: {is_thumb_close},
              is_tilted_left: {is_tilted_left},
              is_tilted_right: {is_tilted_right}
            ''')

        if is_hand_open:
            return "S"
        
        elif is_tilted_left:
            return "L"
        
        elif is_tilted_right:
            return "R"
        
        elif is_fist and is_thumb_close:
            return "F"
        
        elif is_fist and not is_thumb_close:
            return "B"

        # TODO - Make this logic perfect
        elif index_tip_y < middle_tip_y < ring_tip_y < pinky_tip_y and index_tip_x > index_pip_x and middle_tip_x > middle_pip_x and ring_tip_x > ring_pip_x and pinky_tip_x > pinky_pip_x and thumb_tip_y < thumb_ip_y < thumb_mcp_y < thumb_cmc_y < wrist_y:
            return "Q"

        else:
            return "S"

    def get_movement(self):
        """Main function isi function ko call karke data lega."""
        return self.current_gesture

    def detect_hands(self, frame):
        """Frame ko background processor mein bhejta hai."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp = int(time.time() * 1000)
        self.result = self.detector.detect_for_video(mp_image, timestamp)

    def close(self):
        self.detector.close()

class WiFiController:
    def __init__(self):
        self.UDP_IP = "192.168.4.1"
        self.UDP_PORT = 5005

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_to_esp32(self, message):
        try:
            self.socket.sendto(message.encode(), (self.UDP_IP, self.UDP_PORT))
            print(f"Sent command: {message}")
        except Exception as e:
            print(f"Error sending: {e}")
    
def main():
    # Initialization
    cap = cv2.VideoCapture(0)
    gesture_engine = HandGesture()
    wifi_controller = WiFiController()

    print("Control System Online. Press 'q' to quit.")

    initial_time = time.time() * 1000
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        # Frame flip for mirror effect (Important for Left/Right logic)
        frame = cv2.flip(frame, 1)

        # 1. Push frame to background detector
        gesture_engine.detect_hands(frame)

        gesture_engine.update_gesture()

        # 2. Get current movement INSTANTLY (No blocking)
        movement = gesture_engine.get_movement()

        print(f"{time.time()*1000 - initial_time}. Car Status: {movement}")

        # Display (Optional for debugging)
        cv2.putText(frame, f"CMD: {movement}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Gesture Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or movement == 'Q': break

        if movement != 'Q':
            wifi_controller.send_to_esp32(movement)

    gesture_engine.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()