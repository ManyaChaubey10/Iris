import cv2
import mediapipe as mp
import os
import csv

mp_hands = mp.solutions.hands

dataset_path = "Dataset"
output_file = "dataset.csv"

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:

        for label in os.listdir(dataset_path):

            folder = os.path.join(dataset_path, label)

            for img_name in os.listdir(folder):

                img_path = os.path.join(folder, img_name)

                img = cv2.imread(img_path)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = hands.process(imgRGB)

                if results.multi_hand_landmarks:

                    for handLms in results.multi_hand_landmarks:

                        landmark_list = []

                        base_x = handLms.landmark[0].x
                        base_y = handLms.landmark[0].y

                        for lm in handLms.landmark:
                            landmark_list.append(lm.x - base_x)
                            landmark_list.append(lm.y - base_y)

                        writer.writerow(landmark_list + [label])

print("Dataset generated successfully!")