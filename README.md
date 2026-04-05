# Trahymam: Hand-Gesture Controlled ESP32 Robot 🏎️✋

It is an AI-powered robotics project that allows you to control a 4-wheel drive robot car using real-time hand gestures. The system uses a laptop's camera to detect hand landmarks via MediaPipe, processes the gestures to determine movement, and sends commands wirelessly to an ESP32 over a local UDP Wi-Fi network.

## 🌟 Key Features
- **AI Hand Tracking:** Uses MediaPipe Hand Landmarker to identify complex hand shapes.
- **Wireless Control:** High-speed, low-latency communication using UDP over a standalone Access Point.
- **Dynamic Speed Control:** Support for multiple speed levels (1, 2, 3) and situational speed adjustment during turns.
- **Orientation Awareness:** The car tracks its own state (Forward vs. Backward) to ensure turns (Left/Right) are intuitive based on the direction of travel.

---

## 🛠️ Tools & Technologies Used

### Hardware
- **ESP32 Microcontroller:** The "brain" of the car, handling Wi-Fi and motor signals.
- **TB6612FNG Motor Driver:** Efficiently drives 4 DC motors.
- **4WD Chassis:** Standard yellow DC motors with rubber wheels.
- **Laptop:** Serves as the AI processing station.

### Software & Libraries
- **MicroPython:** Running on the ESP32 for easy, readable hardware control.
- **OpenCV:** Handles video capture and frame processing on the laptop.
- **MediaPipe (Google):** Provides the deep learning model for 21-point hand landmark detection.
- **Python (3.9+):** The primary language for the laptop-side controller.
- **Socket Programming:** Used for raw UDP communication between devices.

---

## 📡 System Architecture

The project is split into two halves:

1.  **The Server (ESP32):**
    - Creates a Wi-Fi Access Point named `Trahymam`.
    - Listens on UDP Port `5005` for single-character commands.
    - Decodes commands: `F` (Forward), `B` (Backward), `L` (Left), `R` (Right), `S` (Stop).

2.  **The Client (Laptop):**
    - Captures video frames and flips them for a "mirror" effect.
    - Detects 21 hand landmarks.
    - **Logic Engine:** Translates relative finger positions (e.g., tip vs. knuckle height) into car commands.
    - Sends commands to `192.168.4.1` and 5005 port.



---

## 🖐️ Gesture Mapping

| Gesture | Movement | Logic |
| :--- | :--- | :--- |
| **Open Palm** | **STOP** | All 4 fingers are above their respective knuckles. |
| **Fist + Thumb Tucked** | **FORWARD** | Fingers closed, thumb X-position is near the index finger. |
| **Fist + Thumb Out** | **BACKWARD** | Fingers closed, thumb is extended outward. |
| **Hand Tilted Left** | **LEFT TURN** | Knuckle heights create a downward slope toward the pinky. |
| **Hand Tilted Right** | **RIGHT TURN** | Knuckle heights create an upward slope toward the pinky. |

---

## 🚀 Setup & Installation

### 1. ESP32 Setup
1. Flash **MicroPython v1.20+** onto your ESP32.
2. Save the ESP32 code provided in this repository as `main.py` on the device.
3. Power on the car; it will broadcast the `Trahymam` Wi-Fi network.

### 2. Laptop Setup
1. Ensure you have the `hand_landmarker.task` model file in your project directory.
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Connect your laptop Wi-Fi to the **Trahymam** network.
4. Run the controller:
   ```bash
   uv run gesture_controller.py
   ```

---

## 💡 How this Code Helps Others
- **Education:** Demonstrates how to bridge High-Level AI (MediaPipe) with Low-Level Hardware (MicroPython).
- **UDP Efficiency:** Shows a practical use case for UDP over TCP in robotics where speed is more critical than 100% data delivery.
- **State Management:** The `Wheel` class maintains its own state, preventing the car from performing illegal or confusing maneuvers (like turning left while stopped).

---

## 🏗️ Future Scope
- [ ] Add obstacle avoidance using Ultrasonic sensors.
- [ ] Implement a Web-Dashboard on the ESP32 to monitor battery voltage.
- [ ] Use a PID controller for perfectly straight paths.

**Project Developed by Himanshu** 👨‍💻