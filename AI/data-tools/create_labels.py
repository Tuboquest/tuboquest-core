from ultralytics import YOLO
import os
import cv2

# Load pre-trained model
model = YOLO('yolov8n.pt')

# Image & Label data
image_folder = './val_data'
label_folder = './val_labels'

if not os.path.exists(label_folder):
    os.makedirs(label_folder)

for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(image_folder, filename)
        img = cv2.imread(img_path)

        # Prediction on image
        results = model(img)

        # Name of corresponding label file
        label_filename = os.path.splitext(filename)[0] + '.txt'
        label_filepath = os.path.join(label_folder, label_filename)

        # YOLO formated labels
        with open(label_filepath, 'w') as f:
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls)
                    x_center = box.x_center / img.shape[1]
                    y_center = box.y_center / img.shape[0]
                    width = box.width / img.shape[1]
                    height = box.height / img.shape[0]
                    f.write(f'{cls} {x_center} {y_center} {width} {height}\n')
