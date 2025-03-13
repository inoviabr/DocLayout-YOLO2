import os
import subprocess
import argparse
from pdf2image import convert_from_path
import pytesseract
import shutil
from PIL import Image
import cv2
from doclayout_yolo import YOLOv10

# Defining arguments
parser = argparse.ArgumentParser(description="Pipeline integrado para processamento de PDFs.")
parser.add_argument("--pdf_folder", required=True, type=str, help="Pasta contendo os arquivos PDF")
parser.add_argument("--output_folder", required=True, type=str, help="Pasta para salvar os resultados")
parser.add_argument("--ocr_lang", default="por", type=str, help="Código de idioma para o Tesseract (default: por)")
args = parser.parse_args()

print(" Starting the pipeline...")
print(f" PDF folder: {args.pdf_folder}")
print(f" Output folder: {args.output_folder}")

# Define intermediate and final folders
images_folder = os.path.join(args.output_folder, "imagens")
yolo_output_folder = os.path.join(args.output_folder, "yolo_layouts")
text_regions_folder = os.path.join(yolo_output_folder, "text_regions")
ocr_output_folder = os.path.join(args.output_folder, "ocr_texts")
annotated_layout_folder = os.path.join(args.output_folder, "annotated_layouts")

# Create the necessary folders
os.makedirs(images_folder, exist_ok=True)
os.makedirs(yolo_output_folder, exist_ok=True)
os.makedirs(ocr_output_folder, exist_ok=True)
os.makedirs(annotated_layout_folder, exist_ok=True)

# Function to convert PDFs into images
def convert_pdf_to_images(pdf_path, output_folder, dpi=200, fmt="jpg"):
    print(f"Converting PDF: {pdf_path} -> {output_folder}")
    os.makedirs(output_folder, exist_ok=True)
    images = convert_from_path(
        pdf_path, dpi=dpi, output_folder=output_folder, fmt=fmt,
        output_file=os.path.splitext(os.path.basename(pdf_path))[0] + "_pagina"
    )
    print(f" {len(images)} images generated.")

# Convert all PDFs in the folder into images
for file in os.listdir(args.pdf_folder):
    if file.lower().endswith('.pdf'):
        pdf_path = os.path.join(args.pdf_folder, file)
        pdf_images_folder = os.path.join(images_folder, os.path.splitext(file)[0])
        os.makedirs(pdf_images_folder, exist_ok=True)
        convert_pdf_to_images(pdf_path, pdf_images_folder)

# Perform plain text extraction via YOLO
print("Extracting plain text via YOLO...")
subprocess.run([
    "python",
    "extract_plain_text.py",
    "--input_folder", os.path.abspath(images_folder),
    "--output_folder", os.path.abspath(yolo_output_folder)
], check=True)

# Copy folder structure for OCR (if necessary)
ocr_final_folder = os.path.join(args.output_folder, "ocr_layouts")
shutil.copytree(
    yolo_output_folder, 
    ocr_final_folder, 
    dirs_exist_ok=True
)
print(f"Layouts (plain text) saved in: {ocr_final_folder}")

# Annotate complete images with detected layouts
print("Annotating complete page layouts...")
# Load YOLO template for annotation
model_path = os.path.abspath("doclayout_yolo_docstructbench_imgsz1024.pt")
model = YOLOv10(model_path)

for root, _, files in os.walk(images_folder):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, filename)
            print(f"Annotating the image layout: {image_path}")
            
            # Performs the prediction for the entire image
            det_res = model.predict(image_path, imgsz=1024, conf=0.2, device="cpu")
            # Plot the result over the complete image
            annotated_img = det_res[0].plot(pil=True, line_width=2, font_size=20)
            
            # If annotated_img does not have a 'save' method, convert to PIL Image
            if not hasattr(annotated_img, "save"):
                annotated_img = Image.fromarray(cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))
            
            # Keeps the original folder structure for saving the annotated image
            rel_path = os.path.relpath(image_path, images_folder)
            output_path = os.path.join(annotated_layout_folder, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            annotated_img.save(output_path)
            print(f"Annotated layout saved in: {output_path}")

# Perform OCR with Tesseract on the extracted plain text regions
print("Running OCR on the extracted text regions...")
for file in os.listdir(text_regions_folder):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_image_path = os.path.join(text_regions_folder, file)
        output_txt_path = os.path.join(ocr_output_folder, os.path.splitext(file)[0] + ".txt")
        text = pytesseract.image_to_string(Image.open(input_image_path), lang=args.ocr_lang)
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text extracted and saved in: {output_txt_path}")

print("Pipeline completed! Results in:", args.output_folder)
