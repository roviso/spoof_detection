import math
import time

import cv2
import cvzone
from ultralytics import YOLO
from deepface import DeepFace




confidence = 0.6

cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 640)
cap.set(4, 480)
# cap = cv2.VideoCapture("../Videos/motorbikes.mp4")  # For Video


# model = YOLO("../models/l_version_1_300.pt")

model = YOLO("runs/detect/train/weights/last.pt")



classNames = ["fake", "real"]

prev_frame_time = 0
new_frame_time = 0

img_path = "Dataset/SplitData/val/images/17017554403279805.jpg"

# models = [
#   "VGG-Face", 
#   "Facenet", 
#   "Facenet512", 
#   "OpenFace", 
#   "DeepFace", 
#   "DeepID", 
#   "ArcFace", 
#   "Dlib", 
#   "SFace",
# ]

# metrics = ["cosine", "euclidean", "euclidean_l2"]

# im1_path = "Dataset/SplitData/val/images/17017554403279805.jpg"
# im2_path = "Dataset/SplitData/val/images/17017554377959993.jpg"
# result = DeepFace.verify(img1_path=im1_path,
#                                 img2_path=im2_path,
#                                 model_name=models[2],
#                                 distance_metric=metrics[2])


while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True, verbose=False)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            if conf > confidence:
                
                if classNames[cls] == 'real':
                    print("real ")
                    color = (0,255, 0 )
                    # Extract the detected face region
                    # face_img = img[y1:y2, x1:x2]

                    # Save the detected face temporarily (you may choose a different path)
                    

                    # cv2.imwrite(temp_face_path, face_img)

                    # # Perform face verification
                    

                    # Display the verification result
                    # match_text = "Match" 
                    # # if result['verified'] else "No Match"
                    # cvzone.putTextRect(img, match_text, (x1, y1 - 10),
                    #                    scale=1.5, thickness=3, colorR=color)

                else:
                    color = (0, 0, 255)

                cvzone.cornerRect(img, (x1, y1, w, h),colorC=color,colorR=color)
                cvzone.putTextRect(img, f'{classNames[cls].upper()} {int(conf*100)}%',
                                   (max(0, x1), max(35, y1)), scale=2, thickness=4,colorR=color,
                                   colorB=color)


    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)

    cv2.imshow("Image", img)
    cv2.waitKey(1)