#######################################################################
# FileName			: GenerateAruco.py
# Created By		: Rahul Kedia
# Created On		: 25/03/2020
# Describtion		: This file contains the function which generate 
#					  aruco markers and store them in Markers folder.
#######################################################################

from cv2 import aruco
import cv2


def GenerateAruco():
	ArucoDict = aruco.Dictionary_get(aruco.DICT_6X6_50)

	for i in range(50):			# As 50 sized dictonary is selected
		ArucoImage = aruco.drawMarker(ArucoDict,i, 1000)
		cv2.imwrite("Markers/"+str(i) + ".png", ArucoImage)
