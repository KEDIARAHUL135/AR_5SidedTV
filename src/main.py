#######################################################################
# FileName			: main.py
# Created By		: Rahul Kedia
# Created On		: 25/03/2020
# Describtion		: This is the main file for the project. It call 
#					  all other files and functions in order for code 
#					  to work.
#######################################################################


import cv2
import numpy as np
import DetectAruco as DA
import OverlapImage as OI


def FindPointOnAruco(ArucoCorners, IDs):
	ArucoCornersArranged = np.empty([4, 4, 2], dtype=int)
	ArucoPoint = np.empty([4, 2], dtype=float)

	for i in range(4):
		ArucoCornersArranged[IDs[i]] = ArucoCorners[i]

	# Selecting outer corners of the rectangle formed by aruco.
	# Video will be projected on these points.
	for i in range(4):
		ArucoPoint[i] = ArucoCornersArranged[i][i]

	return ArucoPoint, ArucoCornersArranged


def Distance(P1, P2):
	return (((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2)**0.5)


def FindZLength(ArucoCorners, Image):
	ArucoZLength = []
	for Aruco in ArucoCorners:
		HorEdgeLength = Distance(Aruco[0], Aruco[1])
		VerEdgeLength = Distance(Aruco[0], Aruco[-1])
		A = HorEdgeLength*VerEdgeLength
		B = (((Aruco[1][0] - Aruco[0][0])*(Aruco[-1][0] - Aruco[0][0])) + ((Aruco[1][1] - Aruco[0][1])*(Aruco[-1][1] - Aruco[0][1])))
		#ZLength = (A**2 - B**2)**0.5
		Theta = np.arccos(B/A)
		Sin = np.sin(Theta)
		ZLength = A*Sin/100

		#print("A - {}; B - {}; Z - {}".format(A, B, ZLength))
		ArucoZLength.append(ZLength)

		# PrintingZLength
		cv2.line(Image, (Aruco[0][0], Aruco[0][1]), (Aruco[1][0], Aruco[1][1]), (255, 0, 0), 2)
		cv2.line(Image, (Aruco[0][0], Aruco[0][1]), (Aruco[-1][0], Aruco[-1][1]), (0, 255, 0), 2)
		cv2.line(Image, (Aruco[0][0], Aruco[0][1]), (Aruco[0][0], Aruco[0][1]-int(ZLength)), (0, 0, 255), 2)

	#cv2.imshow("Z-axis", Image)
	return ArucoZLength


def FindCubeVertices(ArucoPoint, ArucoZLength):
	CubeVertices = []
	for i in range(4):
		CubeVertices.append([ArucoPoint[i][0], ArucoPoint[i][1]])
	for i in range(4):
		CubeVertices.append([ArucoPoint[i][0], ArucoPoint[i][1] - 150])

	return CubeVertices


def CallForOverlapping(ArucoVideoFrame, VideoFramesTO, CubeVertices):
	Vertices = np.zeros([4, 2])
	EdgeCentersYCoordinate = [(CubeVertices[0][1] + CubeVertices[1][1])//2,
							  (CubeVertices[1][1] + CubeVertices[2][1])//2,
							  (CubeVertices[2][1] + CubeVertices[3][1])//2,
							  (CubeVertices[3][1] + CubeVertices[0][1])//2]

	SortedEdgeCenters = EdgeCentersYCoordinate.copy()
	SortedEdgeCenters.sort()

	Order = []
	for Value in SortedEdgeCenters:
		for i in range(4):
			if Value == EdgeCentersYCoordinate[i]:
				if not Order.count(i):
					Order.append(i)
					break
	Order.append(4)
	
	Vertices = [[CubeVertices[5], CubeVertices[4], CubeVertices[0], CubeVertices[1]],
				[CubeVertices[6], CubeVertices[5], CubeVertices[1], CubeVertices[2]],
				[CubeVertices[7], CubeVertices[6], CubeVertices[2], CubeVertices[3]],
				[CubeVertices[4], CubeVertices[7], CubeVertices[3], CubeVertices[0]],
				[CubeVertices[4], CubeVertices[5], CubeVertices[6], CubeVertices[7]]]

	Vertices = np.asarray(Vertices)

	Frame = ArucoVideoFrame.copy()
	for i in range(5):
		Frame = OI.OverlapImage(Frame, VideoFramesTO[Order[i]], Vertices[Order[i]])
	
	return Frame

def main():
	# Dictonary - DICT_6X6_50 is used.
	# Reading video
	Cap_ArucoVideo = cv2.VideoCapture('Videos/ArucoVideo.avi')
	Cap_VideoTO1 = cv2.VideoCapture('Videos/Video1.avi')
	Cap_VideoTO2 = cv2.VideoCapture('Videos/Video2.avi')
	Cap_VideoTO3 = cv2.VideoCapture('Videos/Video3.avi')
	Cap_VideoTO4 = cv2.VideoCapture('Videos/Video4.avi')
	Cap_VideoTO5 = cv2.VideoCapture('Videos/Video5.avi')
	
	while(Cap_VideoTO1.isOpened() and Cap_VideoTO2.isOpened() and\
		  Cap_VideoTO3.isOpened() and Cap_VideoTO4.isOpened() and\
		  Cap_VideoTO5.isOpened() and Cap_ArucoVideo.isOpened()):
		ReturnArucoVideo, ArucoVideoFrame = Cap_ArucoVideo.read()
		ReturnVideoTO1, VideoFrameTO1 = Cap_VideoTO1.read()
		ReturnVideoTO2, VideoFrameTO2 = Cap_VideoTO2.read()
		ReturnVideoTO3, VideoFrameTO3 = Cap_VideoTO3.read()
		ReturnVideoTO4, VideoFrameTO4 = Cap_VideoTO4.read()
		ReturnVideoTO5, VideoFrameTO5 = Cap_VideoTO5.read()

		VideoFramesTO = [VideoFrameTO1, VideoFrameTO2, VideoFrameTO3, VideoFrameTO4, VideoFrameTO5]

		if ReturnArucoVideo is False:
			Cap_ArucoVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
		if ReturnVideoTO1 is False:
			Cap_VideoTO1.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
		if ReturnVideoTO2 is False:
			Cap_VideoTO2.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
		if ReturnVideoTO3 is False:
			Cap_VideoTO3.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
		if ReturnVideoTO4 is False:
			Cap_VideoTO4.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
		if ReturnVideoTO5 is False:
			Cap_VideoTO5.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue

		for i in range(5):
			VideoFramesTO[i] = cv2.resize(VideoFramesTO[i], (1024, 576))
		ArucoVideoFrame = cv2.resize(ArucoVideoFrame, (1024, 576))

		ArucoCorners, IDs = DA.DetectAruco(ArucoVideoFrame)

		# Checking if all 4 aruco markers are found
		if IDs is not None:
			if len(IDs) != 4:
				continue
		else:
			continue

		ArucoPoint, ArucoCornersArranged = FindPointOnAruco(ArucoCorners, IDs)
		ArucoZLength = FindZLength(ArucoCornersArranged, ArucoVideoFrame.copy())

		CubeVertices = FindCubeVertices(ArucoPoint, ArucoZLength)
		CubeVertices = np.asarray(CubeVertices)
		FinalFrame = CallForOverlapping(ArucoVideoFrame, VideoFramesTO, CubeVertices)
	
		cv2.imshow("ArucoVideo", ArucoVideoFrame)
		cv2.imshow("FinalFrame", FinalFrame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	Cap_ArucoVideo.release()
	Cap_VideoTO1.release()
	Cap_VideoTO2.release()
	Cap_VideoTO3.release()
	Cap_VideoTO4.release()
	cv2.destroyAllWindows()
