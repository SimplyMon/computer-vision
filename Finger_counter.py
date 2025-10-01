import cv2
import time
import os
import hand_tracking_module as htm

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Folder containing images
path = "finger"

# Check if the folder exists
if not os.path.exists(path):
    print(f"Folder '{path}' does not exist.")
    exit()  # Exit if the folder doesn't exist

# Check if the folder contains any images
myList = os.listdir(path)
if len(myList) == 0:
    print(f"No files found in the folder '{path}'.")
    exit()  # Exit if the folder is empty

overlayList = []
for impath in myList:
    image = cv2.imread(f"{path}/{impath}")
    if image is None:
        print(f"Failed to load image: {impath}")
    else:
        overlayList.append(image)

pTime = 0
# Make sure to pass valid parameters for detection and tracking confidence
detector = htm.handDetector(
    detectionCon=0.75,  # Confidence for detection
    trackCon=0.75,  # Confidence for tracking
)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Check for other fingers
        for id in range(1, 5):  # y axis
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        print(totalFingers)

        # Overlay the image based on finger count
        if totalFingers < len(overlayList):
            h, w, c = overlayList[totalFingers].shape
            img[0:h, 0:w] = overlayList[totalFingers]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(
            img,
            str(totalFingers),
            (45, 375),
            cv2.FONT_HERSHEY_PLAIN,
            10,
            (255, 0, 0),
            25,
        )

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
    )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
