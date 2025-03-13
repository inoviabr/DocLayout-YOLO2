from pdf2image import convert_from_path
import os

# Settings
pdf_path = "/home/inovia/Documentos/crawl/safra/BalPromoDez2018Port2.pdf"
output_folder = "imagens"
dpi = 200
fmt = "jpg"

try:
    # Check if the PDF exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
    
    # Creates the output folder
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Converting PDF: {pdf_path}...")
    
    # Convert PDF to images
    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        output_folder=output_folder,
        fmt=fmt,
        output_file="pagina_",
        paths_only=True
    )
    
    if len(images) == 0:
        print("No image has been generated. Check that the PDF has valid pages.")
    else:
        print(f"Conversion complete! {len(images)} images saved in: {output_folder}")

except Exception as e:
    print(f"Error during conversion: {str(e)}")