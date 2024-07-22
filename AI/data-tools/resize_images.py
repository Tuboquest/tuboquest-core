import cv2
import os

input_folder = './images/duckduckgo_large'
output_folder = './val_data'
target_size = (640, 640)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img = cv2.imread(os.path.join(input_folder, filename))
        if img is not None:
            resized_img = cv2.resize(img, target_size)
            cv2.imwrite(os.path.join(output_folder, filename), resized_img)
        else:
            print(f"Failed to read {filename}")
