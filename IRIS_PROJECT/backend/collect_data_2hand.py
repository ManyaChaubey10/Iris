import cv2
import mediapipe as mp
import csv

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Camera setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

label = input("Enter WORD label (HELLO, YES, etc): ")

count = 0
frame_count = 0
save_interval = 5   # save every 5 frames

with open("dataset_2hand.csv", "a", newline="") as f:
    writer = csv.writer(f)

    while True:
        success, img = cap.read()

        if not success:
            print("Camera error")
            break

        img = cv2.flip(img, 1)
        frame_count += 1

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        # ✅ ONLY accept exactly 2 hands
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:

            landmark_list = []

            # Process both hands
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                base_x = handLms.landmark[0].x
                base_y = handLms.landmark[0].y

                for lm in handLms.landmark:
                    landmark_list.append(lm.x - base_x)
                    landmark_list.append(lm.y - base_y)

            # Ensure exactly 84 values
            if len(landmark_list) == 84:

                if frame_count % save_interval == 0:
                    row = landmark_list + [label]
                    writer.writerow(row)

                    count += 1
                    print(f"Saved {count}")

        cv2.imshow("Collect 2-Hand Data", img)

        if cv2.waitKey(1) == 27:  # ESC to exit
            break

cap.release()
cv2.destroyAllWindows()