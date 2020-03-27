#######################################################################
# FileName			: DetectAruco.py
# Created By		: Rahul Kedia
# Created On		: 25/03/2020
# Describtion		: This file detects the aruco markers in the video 
#				   	  and passes the parameters.
#######################################################################


import cv2
from cv2 import aruco
import numpy as np


def DetectAruco(ArucoFrame):
	GrayFrame = cv2.cvtColor(ArucoFrame, cv2.COLOR_BGR2GRAY)
	ArucoDict = aruco.Dictionary_get(aruco.DICT_6X6_50)
	Parameters =  aruco.DetectorParameters_create()
	Corners, IDs, RejectedImgPoints = aruco.detectMarkers(GrayFrame, ArucoDict, parameters=Parameters)

	ArucoDetectedFrame = aruco.drawDetectedMarkers(ArucoFrame.copy(), Corners, IDs)

	return Corners, IDs