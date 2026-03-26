# 🏎️ Gesture Controlled RC Car (Hand Tracking)

This project uses **MediaPipe's latest Tasks API** and **OpenCV** to control an RC Car using hand gestures. It detects hand landmarks in real-time and translates finger positions into movement commands (Forward, Backward, Stop, etc.).

---

## 🚀 Features
- **Real-time Hand Tracking**: Powered by MediaPipe 0.10+ (Optimized for Apple M-series & modern CPUs).
- **Custom Gesture Logic**: Identifies if fingers are **Up, Down, or Bent** using relative Y-coordinates and buffer zones.
- **Low Latency**: Uses `RunningMode.VIDEO` for smooth tracking without frame drops.

---

## 🛠️ Setup & Installation

### 1. Requirements
- Python 3.9+
- OpenCV
- MediaPipe 0.10.0+

### 2. Install Dependencies
```bash
uv sync
