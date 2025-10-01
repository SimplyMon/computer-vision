import cv2
import dlib
from scipy.spatial import distance
from imutils import face_utils
from playsound import playsound
import threading

# Constants
EAR_THRESHOLD = 0.25
EAR_CONSEC_FRAMES = 20  # Number of frames to check for drowsiness

COUNTER = 0
ALARM_ON = False


# Calculate Eye Aspect Ratio
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# Play alarm sound
def sound_alarm(path="preview.mp3"):
    playsound(path)


# Load face detector and landmark predictor
print("[INFO] Loading predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Start webcam video stream
print("[INFO] Starting video stream...")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        # Visualize eye region
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < EAR_THRESHOLD:
            COUNTER += 1

            if COUNTER >= EAR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True
                    threading.Thread(target=sound_alarm).start()
                cv2.putText(
                    frame,
                    "DROWSINESS DETECTED!",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
        else:
            COUNTER = 0
            ALARM_ON = False

        cv2.putText(
            frame,
            f"EAR: {ear:.2f}",
            (300, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            1,
        )

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
