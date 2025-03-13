# extract_figures.py
import os
import cv2
import argparse
from doclayout_yolo import YOLOv10

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", required=True, type=str, help="Pasta com imagens ORIGINAIS (não anotadas)")
parser.add_argument("--output_folder", required=True, type=str, help="Pasta principal de resultados")
args = parser.parse_args()

# Settings
model_path = os.path.abspath("doclayout_yolo_docstructbench_imgsz1024.pt")
figure_output_folder = os.path.join(args.output_folder, "figure_regions")
os.makedirs(figure_output_folder, exist_ok=True)

# Load model
model = YOLOv10(model_path)

# Process images
for root, _, files in os.walk(args.input_folder):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, filename)
            print(f"\nProcessing: {image_path}")
            
            # Detection of elements
            detections = model.predict(image_path, imgsz=1024, conf=0.25, device="cpu")
            
            # Upload original image
            img = cv2.imread(image_path)
            
            # Extract only pictures
            figure_counter = 0
            for i, cls in enumerate(detections[0].boxes.cls):
                class_name = detections[0].names[int(cls)].lower()
                
                if class_name == "figure":  # Exclusive filter for pictures
                    x1, y1, x2, y2 = map(int, detections[0].boxes.xyxy[i].tolist())
                    figure_roi = img[y1:y2, x1:x2]
                    
                    # Save picture
                    output_filename = f"{os.path.splitext(filename)[0]}_figura_{figure_counter+1}.png"
                    cv2.imwrite(os.path.join(figure_output_folder, output_filename), figure_roi)
                    print(f"Figure detected: {output_filename}")
                    figure_counter += 1

print(f"\nDone! Figures saved in: {figure_output_folder}")