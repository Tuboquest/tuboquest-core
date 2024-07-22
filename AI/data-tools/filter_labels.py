import os

# Path to labels
label_folder = './val_data/labels'

# Class to keep
class_to_keep = '0'

for filename in os.listdir(label_folder):
    if filename.endswith(".txt"):
        label_path = os.path.join(label_folder, filename)

        with open(label_path, 'r') as file:
            lines = file.readlines()

        # Filtering lines to keep (detections)
        filtered_lines = [line for line in lines if line.startswith(class_to_keep)]

        # Rewriting file with filtered lines
        with open(label_path, 'w') as file:
            file.writelines(filtered_lines)

print("Filtrage des labels terminé.")
