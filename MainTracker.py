# ref: https://www.pyimagesearch.com/2018/08/06/tracking-multiple-objects-with-opencv/

from imutils.video import VideoStream
import argparse, imutils, time, cv2
from random import randint

Vpath = 'Quiz.avi' # your video file path
cap = cv2.VideoCapture(Vpath)

cap.set(1,10) # Set first frame = 10 to analyze
success, frame = cap.read()

bboxes = []
colors = [] 

while True:
    bbox = cv2.selectROI('MultiTracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0x80, 0xFF), randint(0x80, 0xFF), randint(0x80, 0xFF)))
    print("q: quit selecting object and start tracking, Other keys: select next object")
    k = cv2.waitKey(0) & 0xFF
    if (k == ord('q')): break
print('Selected bounding boxes {}'.format(bboxes))

multiTracker = cv2.MultiTracker_create()

for bbox in bboxes:
    multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    success, boxes = multiTracker.update(frame)

    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

    cv2.imshow('MultiTracker', frame)

    if cv2.waitKey(1) & 0xFF == 27: break  # quit when Esc pressed
