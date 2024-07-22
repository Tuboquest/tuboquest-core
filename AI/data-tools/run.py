from ultralytics import YOLO
import cv2

# Load model (here the re-trained model)
model = YOLO('runs/detect/asvp_agent_yolov8n/weights/best.pt')

# Initialize video (0 for default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Predict on frame
    results = model(frame)

    for result in results:
        # Convert results to image with annotations
        annotated_frame = result.plot()

        # Display the frame with detections
        cv2.imshow('YOLOv8 Detection', annotated_frame)

    # Break on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop capture and close windows
cap.release()
cv2.destroyAllWindows()
