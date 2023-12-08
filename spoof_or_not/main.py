from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deepface import DeepFace
import math
import cv2
import cvzone
from ultralytics import YOLO
import shutil
import os
from typing import List
import numpy as np
from tensorflow.python.framework import ops



app = FastAPI()



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup_event():
    print("app started")
    global graph
    graph = ops.get_default_graph()
    # do start connection mongodb


@app.on_event("shutdown")
def shutdown_event():
    print("app stoped")
    # do stop connection mongodb


model = YOLO("runs/detect/train5/weights/last.pt")

confidence = 0.6

classNames = ["fake", "real"]

prev_frame_time = 0
new_frame_time = 0



@app.post("/liveness/")
async def liveness_faces(file: UploadFile = File(...)):
    try:
        # Save the uploaded image temporarily
        with open("temp_image.jpg", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read the saved image
        img = cv2.imread("temp_image.jpg")

        if img is None:
            raise ValueError("Invalid image.")

        results = model(img, stream=True, verbose=False)

        liveness_result = "Unknown"
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
                    liveness_result = classNames[cls].upper()
                    break

        # Clean up: remove the temporary file
        os.remove("temp_image.jpg")
        if liveness_result == "REAL":
            status = "success"
        elif liveness_result == "FAKE":
            status = "failed"
        else:
            status = "failed"
        return {"status": status}

    except Exception as e:
        # Clean up even if there's an error
        if os.path.exists("temp_image.jpg"):
            os.remove("temp_image.jpg")
        raise HTTPException(status_code=500, detail=str(e))
    

def read_imagefile(file):
    nparr = np.frombuffer(file, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

metrics = ["cosine", "euclidean", "euclidean_l2"]


@app.post("/analyze")
async def analyzer(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())


    with graph.as_default():

        demography = DeepFace.analyze(image, actions=["age", "gender", "race"])
        # demography = DeepFace.analyze(img, actions=["emotion"])
        print(demography)
    return {"prediction": demography}


@app.post("/verification")
async def verification_route(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    print("reading image 1")
    image1 = read_imagefile(await file1.read())

    print("reading image 2")
    image2 = read_imagefile(await file2.read())


    with graph.as_default():
        print("Varifying Match")
        result = DeepFace.verify(image1, image2)
        print(f"result: {result}")

    return True if result['verified'] == True else False 