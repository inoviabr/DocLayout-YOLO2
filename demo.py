import os
import cv2
import torch
import argparse
from doclayout_yolo import YOLOv10
from PIL import Image
import numpy as np
import glob

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default=None, required=True, type=str)
    parser.add_argument('--image-path', default=None, required=True, type=str)
    parser.add_argument('--res-path', default='outputs', required=False, type=str)
    parser.add_argument('--imgsz', default=1024, required=False, type=int)
    parser.add_argument('--line-width', default=5, required=False, type=int)
    parser.add_argument('--font-size', default=20, required=False, type=int)
    parser.add_argument('--conf', default=0.2, required=False, type=float)
    args = parser.parse_args()
    
    # Automatic device selection
    device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"Using device: {device}")

    model = YOLOv10(args.model)  # Load the official model

    # Checks if the entry is a folder or a single file.
    if os.path.isdir(args.image_path):
        image_files = [f for f in os.listdir(args.image_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        image_paths = [os.path.join(args.image_path, img) for img in image_files]
    else:
        image_paths = [args.image_path]

    # Finds all images in subfolders recursively
    image_paths = glob.glob(os.path.join(args.image_path, '**/*.jpg'), recursive=True) + \
                  glob.glob(os.path.join(args.image_path, '**/*.png'), recursive=True) + \
                  glob.glob(os.path.join(args.image_path, '**/*.jpeg'), recursive=True)

   # Processes each image found
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        
        # Predicts the current image
        det_res = model.predict(image_path, imgsz=args.imgsz, conf=args.conf, device=device)
        
        # Plot the result on the image
        annotated_frame = det_res[0].plot(pil=True, line_width=args.line_width, font_size=args.font_size)
        
        # Set the output path while keeping the original folder structure
        relative_path = os.path.relpath(image_path, args.image_path)  
        output_subfolder = os.path.dirname(relative_path)             
        output_dir = os.path.join(args.res_path, output_subfolder)      

        # Create the folder if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save the annotated image
        output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_res.jpg"
        output_path = os.path.join(output_dir, output_filename)

        # Convert to PIL and save
        pil_image = Image.fromarray(cv2.cvtColor(np.array(annotated_frame), cv2.COLOR_RGB2BGR))
        pil_image.save(output_path, quality=95)

        print(f"Complete layout saved in: {output_path}")
