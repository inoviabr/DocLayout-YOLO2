import os
import cv2
import argparse
from doclayout_yolo import YOLOv10

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", required=True, type=str)
parser.add_argument("--output_folder", required=True, type=str)
args = parser.parse_args()

# Paths
model_path = os.path.abspath("doclayout_yolo_docstructbench_imgsz1024.pt")
text_region_folder = os.path.join(args.output_folder, "text_regions")
os.makedirs(text_region_folder, exist_ok=True)

# Load model
model = YOLOv10(model_path)

# Process images
for root, _, files in os.walk(args.input_folder):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, filename)
            print(f"\n Processing: {image_path}")
            
            # Detection
            det_res = model.predict(image_path, imgsz=1024, conf=0.2, device="cpu") 
            
            # Upload original image
            image = cv2.imread(image_path)
            
            # Extract text regions
            text_count = 0
            for i, cls in enumerate(det_res[0].boxes.cls):
                # Check if the class is “plain text” (case insensitive)
                if det_res[0].names[int(cls)].lower() == "plain text":
                    x1, y1, x2, y2 = map(int, det_res[0].boxes.xyxy[i].tolist())
                    roi = image[y1:y2, x1:x2]
                    
                    # Save the extracted region
                    output_name = f"{os.path.splitext(filename)[0]}_text_{text_count+1}.png"
                    cv2.imwrite(os.path.join(text_region_folder, output_name), roi)
                    print(f" Saved: {output_name}")
                    text_count += 1

print("\n Extraction complete! Text regions saved in:", text_region_folder)
