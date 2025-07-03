import cv2
import numpy as np

# Load pre-trained MobileNet SSD model and class labels
prototxt_path = "deploy.prototxt"
model_path = "mobilenet_iter_73000.caffemodel"


net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Define class labels for detection
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "wall",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "charger", "train", "tvmonitor", "mobile phone", "laptop", "mobile", "paper", "pan"]

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Convert frame to a blob (preprocessing for DNN model)
    blob = cv2.dnn.blobFromImage(cv2.resize(
        frame, (500, 500)), 0.007843, (500, 500), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Loop through detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])  # Class ID
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = f"{CLASSES[idx]}: {confidence*100:.2f}%"
            color = (0, 0, 0)  # Green color for bounding box
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Show output
    cv2.imshow("Object Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
