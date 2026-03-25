# Virtual Keyboard (Gesture Controlled)

A touchless virtual keyboard built using computer vision and hand gesture tracking.

---

## Overview

This project enables typing without a physical keyboard by tracking hand movements through a webcam.
It detects finger positions in real time and uses gesture-based interactions to simulate key presses directly on the system.

---

## Features

* Real-time hand tracking using MediaPipe
* Stable gesture-based typing with anti-shake logic
* Full QWERTY keyboard layout
* Neon-style interactive interface
* Floating word suggestion near the fingertip
* Tap-to-autocomplete using gestures
* Direct system input using PyAutoGUI

---

## Tech Stack

* Python
* OpenCV
* MediaPipe
* Tkinter
* PyAutoGUI
* Pillow

---

## How It Works

* The webcam captures live video input
* Hand landmarks are detected using MediaPipe
* The index finger is used as a pointer
* A pinch gesture (distance between fingers) acts as a click
* Stability tracking and hover timing improve accuracy and reduce unintended inputs

---

## Highlights

* Touchless interaction
* Real-time performance
* Minimal and responsive interface
* Demonstrates gesture-based human-computer interaction

---

## Note

Performance depends on lighting conditions and camera quality for accurate hand detection.
