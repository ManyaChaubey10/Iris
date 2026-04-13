from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import mediapipe as mp
import pickle
import base64
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained models
try:
    letter_model = pickle.load(open("asl_model.pkl", "rb"))
except Exception as e:
    print("Could not load ASL letter model:", e)
    letter_model = None

try:
    word_model = pickle.load(open("word_model.pkl", "rb"))
except Exception as e:
    print("Could not load ASL word model:", e)
    word_model = None

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, # Process each frame independently
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

@app.route("/")
def home():
    return "IRIS Backend Running"

@app.route("/predict_frame", methods=["POST"])
def predict_frame():
    if not letter_model or not word_model:
        return jsonify({"error": "Models not loaded"}), 500
        
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400
        
    image_data = data['image']
    try:
        # Extract base64 part
        if "," in image_data:
            image_data = image_data.split(",")[1]
            
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None:
             return jsonify({"error": "Could not decode image"}), 400
             
        # Flip image to match training data
        img = cv2.flip(img, 1)
             
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        prediction = None
        
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            landmark_list = []
            
            for handLms in results.multi_hand_landmarks:
                base_x = handLms.landmark[0].x
                base_y = handLms.landmark[0].y
                
                for lm in handLms.landmark:
                    landmark_list.append(lm.x - base_x)
                    landmark_list.append(lm.y - base_y)
                    
            if num_hands == 1:
                prediction = letter_model.predict([landmark_list])[0]
            elif num_hands == 2:
                if len(landmark_list) < 84:
                    landmark_list += [0] * (84 - len(landmark_list))
                prediction = word_model.predict([landmark_list])[0]
                
        return jsonify({"prediction": prediction})
        
    except Exception as e:
        print("Error processing frame:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)