#######################################################################
# FileName			: OverlapImage.py
# Created By		: Rahul Kedia
# Created On		: 26/03/2020
# Describtion		: This file overlaps the video on aruco video via 
#				 	  aruco markers detected.
#######################################################################


import cv2
import numpy as np


def ProjectiveTransform(FrameToBeOverlaped, ArucoPoint):
	Height, Width = FrameToBeOverlaped.shape[:2]
	InitialPoints = np.float32([[0, 0], [Width-1, 0], [0, Height-1], [Width-1, Height-1]])
	FinalPoints = np.float32([[ArucoPoint[0][0], ArucoPoint[0][1]], 
							  [ArucoPoint[1][0], ArucoPoint[1][1]], 
							  [ArucoPoint[3][0], ArucoPoint[3][1]], 
							  [ArucoPoint[2][0], ArucoPoint[2][1]]])

	ProjectiveMatrix = cv2.getPerspectiveTransform(InitialPoints, FinalPoints)
	TransformedFrame = cv2.warpPerspective(FrameToBeOverlaped, ProjectiveMatrix, (Width, Height))
	
	return TransformedFrame, FinalPoints


def OverayImage(TransformedFrame, ArucoVideoFrame, ArucoPoint):
	MaskArucoVideoFrame = np.zeros(ArucoVideoFrame.shape, dtype=np.uint8)

	cv2.fillConvexPoly(MaskArucoVideoFrame, ArucoPoint.astype(np.int32), (255, )*ArucoVideoFrame.shape[2])

	MaskArucoVideoFrame = cv2.bitwise_not(MaskArucoVideoFrame)
	BlackFrameForOverlap = cv2.bitwise_and(ArucoVideoFrame, MaskArucoVideoFrame)

	FinalImage = cv2.bitwise_or(TransformedFrame, BlackFrameForOverlap)

	return FinalImage


def OverlapImage(ArucoVideoFrame, FrameToBeOverlaped, ArucoPoint):
	ArucoPoint = ArucoPoint.astype(float)

	TransformedFrame, FinalPoints = ProjectiveTransform(FrameToBeOverlaped, ArucoPoint)
	Final = OverayImage(TransformedFrame, ArucoVideoFrame, ArucoPoint)

	return Final
	