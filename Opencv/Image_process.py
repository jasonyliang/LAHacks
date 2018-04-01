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
import base64
import json
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from timeit import default_timer as timer

def main():
    
    dir_path = 'C://Users//Ryan_Siv//Documents//GitHub//LAHacks'
    api_key = 'My First Project-e65c2d409577.json'
    client = authenticate(dir_path, api_key)
    jason = cv2.imread('D://Misc Projects//AutoSombrero//jason.jpg')
#    start = timer()
#    nose_coords = process_images(jason, client)
#    end = timer()
#    print(nose_coords, end - start)
    frame_width = 680
    frame_height = 480
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 15) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    while True:
       ret, frame = cap.read()
       cv2.imshow('img',frame)
       
       #Note Image is mirrored so flip the coordinates
       
       if cv2.waitKey(1) & 0xFF == ord('y'):
           break
       
    cap.release()
    cv2.destroyAllWindows()
       
    
    
    

def authenticate(dir_path, api):
    api_key = os.path.join(dir_path,api)
    credentials = service_account.Credentials.from_service_account_file(api_key)
    client = vision.ImageAnnotatorClient(credentials = credentials)
    return client

def process_images(image, client):
    bit_arr = cv2.imencode('.jpg', image)[1].tostring()
    content = types.Image(content=bit_arr)
    response = client.face_detection(image = content)
    faces = response.face_annotations
    Nose_tip_coords = faces[0].landmarks[7]
    return((Nose_tip_coords.position.x,Nose_tip_coords.position.y,Nose_tip_coords.position.z))
    
main()