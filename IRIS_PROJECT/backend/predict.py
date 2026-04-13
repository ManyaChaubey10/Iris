import cv2
import mediapipe as mp
import pickle
import pyttsx3
import threading
from collections import deque
import time

# =========================
# LOAD MODELS
# =========================
letter_model = pickle.load(open("asl_model.pkl", "rb"))
word_model = pickle.load(open("word_model.pkl", "rb"))

# =========================
# SPEECH ENGINE
# =========================
engine = pyttsx3.init()
last_prediction = None
last_spoken_time = 0

def speak(text):
    engine.say(text)
    engine.runAndWait()

# =========================
# BUFFER (SMOOTHING)
# =========================
prediction_buffer = deque(maxlen=10)

# =========================
# MEDIAPIPE SETUP
# =========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# =========================
# CAMERA SETUP
# =========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

# =========================
# MAIN LOOP
# =========================
while True:
    success, img = cap.read()

    if not success:
        print("Camera error")
        break

    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        num_hands = len(results.multi_hand_landmarks)
        landmark_list = []

        # Extract landmarks
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            base_x = handLms.landmark[0].x
            base_y = handLms.landmark[0].y

            for lm in handLms.landmark:
                landmark_list.append(lm.x - base_x)
                landmark_list.append(lm.y - base_y)

        # =========================
        # 1 HAND → LETTER MODEL
        # =========================
        if num_hands == 1:
            model_used = "Letter"
            prediction = letter_model.predict([landmark_list])[0]

        # =========================
        # 2 HAND → WORD MODEL
        # =========================
        elif num_hands == 2:
            model_used = "Word"

            # Ensure 84 values
            if len(landmark_list) < 84:
                landmark_list += [0] * (84 - len(landmark_list))

            prediction = word_model.predict([landmark_list])[0]

        # =========================
        # SMOOTHING
        # =========================
        prediction_buffer.append(prediction)
        pred = max(set(prediction_buffer), key=prediction_buffer.count)
        confidence = prediction_buffer.count(pred) / len(prediction_buffer)

        # =========================
        # DISPLAY (SMART UI)
        # =========================
        cv2.putText(img, f"{pred}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)

        cv2.putText(img, f"Confidence: {int(confidence*100)}%", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)


        # =========================
        # SPEAK (CONTROLLED)
        # =========================
        current_time = time.time()

        if pred != last_prediction and confidence > 0.75 and (current_time - last_spoken_time > 2):
            threading.Thread(target=speak, args=(pred,), daemon=True).start()
            last_prediction = pred
            last_spoken_time = current_time

    # =========================
    # SHOW WINDOW
    # =========================
    cv2.imshow("ASL Recognition System", img)

    if cv2.waitKey(1) == 27:
        break

# =========================
# CLEANUP
# =========================
cap.release()
cv2.destroyAllWindows()