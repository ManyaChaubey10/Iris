import cv2
import mediapipe as mp
import numpy as np
import pickle

# load trained model
model = pickle.load(open("digits_model.pkl", "rb"))

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
) as hands:

    while True:

        success, img = cap.read()
        if not success:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:

            for handLms in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                h, w, _ = img.shape

                x_list = []
                y_list = []

                for lm in handLms.landmark:
                    x_list.append(int(lm.x * w))
                    y_list.append(int(lm.y * h))

                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)

                hand_img = img[ymin:ymax, xmin:xmax]

                if hand_img.size != 0:

                    hand_img = cv2.resize(hand_img, (64, 64))
                    hand_img = cv2.cvtColor(hand_img, cv2.COLOR_BGR2GRAY)

                    hand_img = hand_img.flatten().reshape(1, -1)

                    prediction = model.predict(hand_img)

                    digit = np.argmax(prediction)

                    cv2.putText(
                        img,
                        f"Prediction: {digit}",
                        (10,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        2
                    )

        cv2.imshow("Digit Recognition", img)

        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()