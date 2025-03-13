<div align="center">
<h1>DocLayout-YOLO Enhanced: Advanced Document Analysis Pipeline</h1>

[![Original Project](https://img.shields.io/badge/Based%20on-DocLayout--YOLO-brightgreen)](https://github.com/opendatalab/DocLayout-YOLO)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

## Overview
This enhanced fork of DocLayout-YOLO provides a comprehensive document processing pipeline with additional functionalities for end-to-end document analysis. The implementation extends the original framework with improved batch processing capabilities, integrated OCR support, and workflow automation features while maintaining compatibility with the base model architecture.

## Key Enhancements
### Core Features
- **Integrated PDF-to-Text Pipeline**
  - Automated PDF-to-image conversion
  - Hierarchical directory structure preservation
  - Multi-language OCR integration
- **Extended Functionality**
  - Batch processing with GPU acceleration
  - Text region extraction and classification
  - Duplicate processing prevention
- **Usability Improvements**
  - Configurable parameters for diverse use cases
  - Cross-platform compatibility
  - Comprehensive error handling

## Installation
### Prerequisites


Model Download

    # Download pretrained model
    wget https://huggingface.co/juliozhao/DocLayout-YOLO-DocStructBench/resolve/main/doclayout_yolo_docstructbench_imgsz1024.pt
  
  
  pdf2image pytesseract torch>=2.0.0 ultralytics>=8.0.0
  
  Quick Start
    Full Processing Pipeline
    
    python pipeline.py \
      --pdf_folder input_documents \
      --output_folder analysis_results \
      --ocr_lang eng

Text Region Extraction

      python extract_plain_text.py \
      --input_folder document_images \
      --output_folder extracted_regions

Batch Image Processing
  
    python process_images.py \
    --model doclayout_yolo_docstructbench_imgsz1024.pt \
    --image-path input_images \
    --res-path processed_output

Project Structure
 
      .
      ├── pipeline.py               # Main processing pipeline
      ├── extract_plain_text.py     # Text region extraction
      ├── process_images.py         # Batch image processor
      ├── demo.py                   # Modified inference script
      └── pdf_convert/
          ├── pdfimage.py           # PDF conversion module


Implementation Details
Core Modules
pipeline.py
Function: Orchestrates complete document processing workflow
Features:

PDF to image conversion (300-600 DPI support)

Layout detection with hierarchical output

Tesseract OCR integration

Multi-threaded processing

# Parameters:

      |    Argument     |       Description         |   Default      
      | --pdf_folder    |  Input PDF directory	|   Required  
      | --output_folder |  Results directory	|   Required  
      | --ocr_lang      |  Tesseract language code  |    eng        
      
      
     

Project Execution
Basic Workflow

# Process images through pipeline
python pipeline.py \
    --pdf_folder "your pdf folder" \
    --output_folder "folder for view results"

Function: Extracts and classifies text regions
Detection Capabilities:
      * Paragraphs
      * Headers
      * Tables
      * Captions

Output:
       * Region images with metadata
       * CSV index of detected elements

utils/pdfimage.py

Function: PDF conversion engine

Supported Formats:
  *JPEG (85-100 quality levels)
  *PNG (lossless compression)
  *TIFF (multi-page support)

Advanced Configuration

# Performance Optimization 
     Example GPU configuration
      model.predict(
          image_path,
          imgsz=2048,
          conf=0.25,
          device="cuda:0",
          half_precision=True
      )

# OCR Language Support

    Language	  |     Code	     |    Requirements
    -----------------------------------------------------
    English	    |     eng	       |    Default
    -----------------------------------------------------
    Portuguese  |	    por	       |    tesseract-ocr-por
    -----------------------------------------------------
    Spanish	    |     spa	       |    tesseract-ocr-spa
    -----------------------------------------------------

# Modification Overview
  
    Original File	           Enhancements      
    ------------------------------------------------------------------------------
    demo.py	                 Added directory preservation, process tracking
    ------------------------------------------------------------------------------
    format_docsynth300k.py	 Improved error handling, Windows compatibility
    -------------------------------------------------------------------------------
    New Modules	             pipeline.py, extract_plain_text.py, process_images.py
    -------------------------------------------------------------------------------

Contribution Guidelines

# We welcome contributions through:
  
    1.Issue reporting
  
    2.Feature requests
  
    3.Pull requests

Please follow standard GitHub workflow:

      git checkout -b feature/new-feature
      git commit -m "Descriptive message"
      git push origin feature/new-feature
    
    License
      This project maintains the original MIT License. For commercial use inquiries, please contact the maintainers.
    
    Documentation
  For original model architecture and training details, consult the https://github.com/opendatalab/DocLayout-YOLO.


