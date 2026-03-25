import cv2
import mediapipe as mp
import time
import math
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk

# -------------------- INIT --------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Keyboard layout
keys = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM")
]

# -------------------- GLOBALS --------------------
typed_text = ""
hover_start_time = 0
stable_threshold = 0.7
prev_positions = []

# Suggestion dictionary
dictionary = ["hello", "help", "helmet", "hey", "good", "great",
              "game", "python", "project", "keyboard", "vision"]

# -------------------- FUNCTIONS --------------------
def draw_keyboard(img):
    key_w, key_h = 45, 45
    spacing = 5
    start_x, start_y = 20, 80
    boxes = []

    for r, row in enumerate(keys):
        for c, key in enumerate(row):
            x = start_x + c * (key_w + spacing)
            y = start_y + r * (key_h + spacing)
            boxes.append((x, y, x + key_w, y + key_h, key))

    y = start_y + 3 * (key_h + spacing)
    space_w = int(key_w * 5)
    back_w = int(key_w * 2)
    enter_w = int(key_w * 2)

    boxes.append((start_x, y, start_x + space_w, y + key_h, " "))
    boxes.append((start_x + space_w + 10, y,
                  start_x + space_w + 10 + back_w, y + key_h, "BACK"))
    boxes.append((start_x + space_w + back_w + 20, y,
                  start_x + space_w + back_w + 20 + enter_w, y + key_h, "ENTER"))
    return img, boxes


def draw_neon_key(frame, x1, y1, x2, y2, label, active=False):
    if active:
        color = (0, 255, 0)
        glow = (0, 100, 0)
    else:
        color = (255, 0, 255)
        glow = (100, 0, 100)

    for i in range(5):
        cv2.rectangle(frame, (x1-i, y1-i), (x2+i, y2+i), glow, 1)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    cv2.putText(frame, label, (x1+5, y1+30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def get_suggestion(text):
    last_word = text.split(" ")[-1]
    matches = [w for w in dictionary if w.startswith(last_word)]
    return matches[0] if matches and last_word != "" else None


# -------------------- TKINTER --------------------
root = tk.Tk()
root.title("🔥 AI Virtual Keyboard")
root.attributes('-topmost', True)

canvas_width, canvas_height = 640, 480
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

cap = cv2.VideoCapture(0)
cap.set(3, canvas_width)
cap.set(4, canvas_height)

# -------------------- MAIN LOOP --------------------
def update_frame():
    global hover_start_time, prev_positions, typed_text

    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    frame, key_boxes = draw_keyboard(frame)

    hover_key = None
    suggestion = None
    box_coords = None

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            x_tip = int(handLms.landmark[8].x * canvas_width)
            y_tip = int(handLms.landmark[8].y * canvas_height)
            x_mid = int(handLms.landmark[12].x * canvas_width)
            y_mid = int(handLms.landmark[12].y * canvas_height)

            cv2.circle(frame, (x_tip, y_tip), 6, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (x_mid, y_mid), 6, (255, 255, 0), cv2.FILLED)

            dist = math.hypot(x_mid - x_tip, y_mid - y_tip)

            # -------- Stability --------
            prev_positions.append((x_tip, y_tip))
            if len(prev_positions) > 5:
                prev_positions.pop(0)

            movement = sum(
                math.hypot(prev_positions[i][0] - prev_positions[i-1][0],
                           prev_positions[i][1] - prev_positions[i-1][1])
                for i in range(1, len(prev_positions))
            )

            is_stable = movement < 20

            # -------- Suggestion --------
            suggestion = get_suggestion(typed_text)

            if suggestion:
                box_x1 = x_tip + 20
                box_y1 = y_tip - 40
                box_x2 = box_x1 + 120
                box_y2 = box_y1 + 35
                box_coords = (box_x1, box_y1, box_x2, box_y2)

                cv2.rectangle(frame, (box_x1-2, box_y1-2),
                              (box_x2+2, box_y2+2), (0, 100, 0), 2)
                cv2.rectangle(frame, (box_x1, box_y1),
                              (box_x2, box_y2), (0, 255, 0), 2)

                cv2.putText(frame, suggestion, (box_x1+5, box_y2-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # -------- Suggestion Click --------
            if suggestion and box_coords:
                x1b, y1b, x2b, y2b = box_coords
                if x1b < x_tip < x2b and y1b < y_tip < y2b:
                    if is_stable and dist < 30:
                        last_word = typed_text.split(" ")[-1]
                        typed_text = typed_text[:-len(last_word)] + suggestion + " "
                        pyautogui.write(suggestion[len(last_word):] + " ")
                        hover_start_time = 0
                        return

            # -------- Key detection --------
            for (x1, y1, x2, y2, key) in key_boxes:
                if x1 < x_tip < x2 and y1 < y_tip < y2:
                    hover_key = (x1, y1, x2, y2, key)

                    if is_stable:
                        if hover_start_time == 0:
                            hover_start_time = time.time()

                        if time.time() - hover_start_time > stable_threshold:
                            if dist < 30:
                                if key == "BACK":
                                    typed_text = typed_text[:-1]
                                    pyautogui.press("backspace")

                                elif key == " ":
                                    typed_text += " "
                                    pyautogui.press("space")

                                elif key == "ENTER":
                                    typed_text = ""
                                    pyautogui.press("enter")

                                else:
                                    typed_text += key.lower()
                                    pyautogui.write(key.lower())

                                hover_start_time = 0
                    else:
                        hover_start_time = 0

                    break

    # -------- Draw keyboard --------
    for (x1, y1, x2, y2, key) in key_boxes:
        label = "SPACE" if key == " " else key
        active = hover_key and (x1, y1, x2, y2, key) == hover_key
        draw_neon_key(frame, x1, y1, x2, y2, label, active)

    # -------- Typed text --------
    cv2.putText(frame, typed_text[-30:], (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # -------- Render --------
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img_pil)
    canvas.imgtk = imgtk
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

    root.after(10, update_frame)


# -------------------- RUN --------------------
root.after(0, update_frame)
root.mainloop()
cap.release()
