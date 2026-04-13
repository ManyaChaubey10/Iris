import cv2
import mediapipe as mp
import csv

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:

        success, img = cap.read()
        if not success:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        landmark_list = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                # Wrist landmark (base point)
                base_x = handLms.landmark[0].x
                base_y = handLms.landmark[0].y

                # Normalize landmarks
                for lm in handLms.landmark:
                    landmark_list.append(lm.x - base_x)
                    landmark_list.append(lm.y - base_y)

        cv2.imshow("ASL Dataset Collector", img)

        key = cv2.waitKey(1)

        # Save dataset with dynamic label
        if key != -1 and landmark_list:

            label = chr(key).upper()

            with open("dataset.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(landmark_list + [label])

            print("Saved:", label)

        # ESC to exit
        if key == 27:
            break


cap.release()
cv2.destroyAllWindows()