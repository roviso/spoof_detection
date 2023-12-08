import io
from PIL import Image
from typing import List
from fastapi import FastAPI, File, UploadFile
from deepface import DeepFace
from tensorflow.python.framework import ops
import tensorflow as tf
from io import BytesIO
import numpy as np
import cv2

app = FastAPI()


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


@app.get("/")
def read_root():
    return {"Hello": "World"}



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