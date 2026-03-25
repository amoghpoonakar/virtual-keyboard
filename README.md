# 🔥 Virtual Keyboard (Gesture Controlled)

A touchless virtual keyboard built using computer vision and hand gesture tracking.

---

## 🧠 Overview

This project allows you to type without using a physical keyboard by tracking hand movements through a webcam.

It detects finger positions in real time and uses gesture-based interactions to simulate key presses directly on your system.

---

## ⚙️ Features

* ✋ Real-time hand tracking using MediaPipe
* 🎯 Stable gesture-based typing (anti-shake logic)
* ⌨️ Full QWERTY keyboard layout
* ✨ Neon-style interactive UI
* 💡 Floating word suggestion near fingertip
* ⚡ Tap-to-autocomplete using gestures
* 🖥️ Direct system input via PyAutoGUI

---

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe
* Tkinter
* PyAutoGUI
* Pillow

---

## 💡 How It Works

* The webcam captures live video input
* Hand landmarks are detected using MediaPipe
* The index finger acts as a pointer
* A pinch gesture (distance between fingers) is used as a click
* Stability + hover timing ensures accurate key presses

---

## 🚀 Highlights

* No physical interaction required
* Real-time performance
* Clean and responsive UI
* Demonstrates gesture-based human-computer interaction

---

## 📌 Note

Performance depends on lighting conditions and camera quality for accurate hand detection.
