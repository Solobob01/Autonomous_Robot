import cv2
import numpy as np

def createGreenMask(frame):
	lower_bound = np.array([50, 20, 20])
	upper_bound = np.array([100, 255, 255])
	mask = cv2.inRange(frame, lower_bound, upper_bound)
	_, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
	return mask1

def drawContureOverBottle(mask, frame):
	x, y, w, h = -1, -1, -1, -1
	cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	maxArea = 0
	maxPos = (x, y, w, h)
	#print(cnts)
	for c in cnts:
		x = 600
		if cv2.contourArea(c) > x:
			x, y, w, h = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
		if cv2.contourArea(c) > maxArea and x != 600:
			maxArea = cv2.contourArea(c)
			maxPos = (x, y, w, h)
	cv2.imshow("Processed image", frame)
	return maxPos

def processFrame(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = createGreenMask(hsv)
	return drawContureOverBottle(mask ,frame)
