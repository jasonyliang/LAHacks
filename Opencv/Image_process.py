# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:43:19 2018

@author: Ryan_Siv
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import cv2
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from breakout1 import Brickgame


def main():
    
    dir_path = 'C://Users//Ryan_Siv//Documents//GitHub//LAHacks'
    api_key = 'My First Project-e65c2d409577.json'
    client = authenticate(dir_path, api_key)
#    jason = cv2.imread('D://Misc Projects//AutoSombrero//jason.jpg')
#    start = timer()
#    nose_coords = process_images(jason, client)
#    end = timer()
#    print(nose_coords, end - start)
    
    #Setting Image size to match Game Window Size
    frames = Brickgame.screen_dim
    
    ## Camera Set-up
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 15) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frames[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frames[1])
    
    ## Classifier S
    
    nose_cascade = cv2.CascadeClassifier('./haarcascade_mcs_nose.xml')
    
    ## Main Loop
    while True:
    # Retrieve Camera Frames
       ret, frame = cap.read()
       coords = process_test(frame,nose_cascade)
       cv2.imshow('img',frame)
       vector = convert_coords(coords, frames)
       
       
       
       if cv2.waitKey(1) & 0xFF == ord('y'):
           break
       
    cap.release()
    cv2.destroyAllWindows()
       
    

    
    

def authenticate(dir_path, api):
    ## Load API Information from .json
    api_key = os.path.join(dir_path,api)
    credentials = service_account.Credentials.from_service_account_file(api_key)
    
    ## Create Instance of Image Annotater with Credentials
    client = vision.ImageAnnotatorClient(credentials = credentials)
    return client

def process_images(image, client):
    ## Convert CV2 Image/numpy img to bitarray
    bit_arr = cv2.imencode('.jpg', image)[1].tostring()
    # Base 64 Encode bit array
    content = types.Image(content=bit_arr)
    # Send to API for extraction
    response = client.face_detection(image = content)
    faces = response.face_annotations
    Nose_tip_coords = faces[0].landmarks[7] # Extract Nose Tip Coordinates
    return((Nose_tip_coords.position.x,Nose_tip_coords.position.y,Nose_tip_coords.position.z))
    
def process_test(image, classifier):
    """
    Temporary Test function using openCV for prototyping before switching to google cloud API
    """
    img = classifier.detectMultiScale(image)
    for (x,y,w,h) in img:
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 3)
        return ((x+w/2, y+h/2,0))
    return None
    
def convert_coords(face_coords,frames):
    """
    Converts face coords into vectors for game control.
    """
    ## reverse coordinates
    frame_width = frames[0]
    divisions = 8
    interval = frame_width/divisions
    if face_coords:
        x = face_coords[0]
        nose_coord = (x- frame_width/2)
        vector = int(nose_coord // interval) + int(round((nose_coord % interval)/interval))
        return vector 
    else:
        return 0
    

 
main()