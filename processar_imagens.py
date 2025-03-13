import os
import cv2
from doclayout_yolo import YOLOv10

# Trained model path
model_path = "doclayout_yolo_docstructbench_imgsz1024.pt"

# Path to the folder where the images are
image_folder = "/home/inovia/Documentos/Pfd_convert/imagens"

# Create a folder to store the results
output_folder = os.path.join(image_folder, "resultados")
os.makedirs(output_folder, exist_ok=True)

# Load the YOLO model
model = YOLOv10(model_path)

# Process all the images in the folder
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')): 
        image_path = os.path.join(image_folder, filename)
        output_path = os.path.join(output_folder, f"result_{filename}")

        # Checks if the image has already been processed
        if os.path.exists(output_path):
            print(f" {filename} has already been processed, next...")
            continue

        # Make the prediction
        det_res = model.predict(image_path, imgsz=1024, conf=0.2, device="cuda:0")

        # Write down and save the result
        annotated_frame = det_res[0].plot(pil=True, line_width=5, font_size=20)
        annotated_frame.save(output_path)

        print(f"Processed: {filename} -> {output_path}")

print("Processing complete! Check the 'results' folder'.")
