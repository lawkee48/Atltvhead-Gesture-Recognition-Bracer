# Predict_Gesture.py
# Description: Recieved Data from ESP32 Micro via the AGRB-Training-Data-Capture.ino file, make gesture prediction  
# Written by: Nate Damen
# Created on July 13th 2020

import numpy as np 
import pandas as pd 
import datetime
import re
import os, os.path
import time
import random
import tensorflow as tf
import serial

PORT = "/dev/ttyUSB0"
#PORT = "/dev/ttyUSB1"
#PORT = "COM8"

serialport = None
serialport = serial.Serial(PORT, 115200, timeout=0.05)

#load Model
model = tf.keras.models.load_model('../Model/cnn_model.h5')

#Get Data from imu. Waits for incomming data and data stop
def get_imu_data():
    global serialport
    if not serialport:
        # open serial port
        serialport = serial.Serial(PORT, 115200, timeout=0.05)
        # check which port was really used
        print("Opened", serialport.name)
        # Flush input
        time.sleep(3)
        serialport.readline()

    # Poll the serial port
    line = str(serialport.readline(),'utf-8')
    if not line:
        return None
    #print(line)
    #if not "Uni:" in line:
        #return None
    vals = line.replace("Uni:", "").strip().split(',')
    #print(vals)
    if len(vals) != 7:
        return None
    try:
        vals = [float(i) for i in vals]
    except ValueError:
        return ValueError
    #print(vals)
    return vals

# Create Reshape function for each row of the dataset
def reshape_function(data):
    reshaped_data = tf.reshape(data, [-1, 3, 1])
    return reshaped_data

# header for the incomming data
header = ["deltaTime","Acc_X","Acc_Y","Acc_Z","Gyro_X","Gyro_Y","Gyro_Z"]

#Create a way to see the length of the data incomming, needs to be 760 points. Used for testing incomming data
def dataFrameLenTest(data):
    df=pd.DataFrame(data,columns=header)
    x=len(df[['Acc_X','Acc_Y','Acc_Z']].to_numpy())
    print(x)
    return x

#Create a pipeline to process incomming data for the model to read and handle
def data_pipeline(data_a):
    df = pd.DataFrame(data_a, columns = header)
    temp=df[['Acc_X','Acc_Y','Acc_Z']].to_numpy()
    tensor_set = tf.data.Dataset.from_tensor_slices(
        (np.array([temp.tolist()],dtype=np.float64)))
    tensor_set_cnn = tensor_set.map(reshape_function)
    tensor_set_cnn = tensor_set_cnn.batch(192)
    return tensor_set_cnn

#define Gestures, current data, temp data holder, a first cylce boolean,
gest_id = {0:'single_wave', 1:'fist_pump', 2:'random_motion', 3:'speed_mode'}
data = []
dataholder=[]
dataCollecting = False
gesture = ''
old_gesture = ''

#flush the serial port
serialport.flush()

while(1):
    dataholder = get_imu_data()
    if dataholder != None:
        dataCollecting=True
        data.append(dataholder)
    if dataholder == None and dataCollecting == True:
        if len(data) == 760:
            prediction = np.argmax(model.predict(data_pipeline(data)), axis=1)
            gesture=gest_id[prediction[0]]
            print(gesture)
        data = []
        dataCollecting = False
        old_gesture=gesture
