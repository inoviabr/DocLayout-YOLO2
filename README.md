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
  - **<<Multi-element extraction>>** (text, figures, tables) **<<<**
  - Text and figure region extraction **<<<**
  - Duplicate processing prevention

## Installation
### Prerequisites

```bash
# Dependencies
pdf2image pytesseract torch>=2.0.0 ultralytics>=8.0.0
```

## Quick Start
### Full Processing Pipeline
```bash
python pipeline.py \
  --pdf_folder input_documents \
  --output_folder analysis_results \
  --ocr_lang eng
```

### **<<Figure Extraction>>** **<<<**
```bash
python extract_figures.py \
  --input_folder document_images \
  --output_folder extracted_figures
```

### Text Region Extraction
```bash
python extract_plain_text.py \
  --input_folder document_images \
  --output_folder extracted_regions
```

## Project Structure
```
.
├── pipeline.py               # Main processing pipeline
├── extract_plain_text.py     # Text region extraction
├── **<<extract_figures.py>>**    # Figure extraction **<<<**
├── process_images.py         # Batch image processor
└── pdf_convert/
    ├── pdfimage.py           # PDF conversion module
```

## Implementation Details
### Core Modules
#### **<<extract_figures.py>>** **<<<**
```python
Function: Extracts graphical elements from documents
Features:
  - Figure detection using YOLO model
  - Automatic region cropping
  - Conflict-free naming convention

# Usage:
python extract_figures.py \
  --input_folder scanned_pages \
  --output_folder graphical_elements
```

### Detection Capabilities
| Element Type    | Detection Script          | Output Format |
|-----------------|---------------------------|---------------|
| Text Regions    | extract_plain_text.py     | PNG + CSV     |
| **<<Figures>>** | **<<extract_figures.py>>**| PNG + Log     | **<<<**
| Tables          | pipeline.py               | PNG + JSON    |

## Advanced Configuration
### Model Output Types
```python
Supported element classes:
- 'plain_text'    # Paragraphs and headers
- 'figure'        # Charts and diagrams **<<<**
- 'table'         # Tabular data
- 'caption'       # Image descriptions
```

## Modification Overview
| Original File       | Enhancements                      |
|---------------------|-----------------------------------|
| **<<New Module>>**  | **<<extract_figures.py>>**        | **<<<**
| pipeline.py         | Added figure extraction support   | **<<<**

## Documentation
 For original model architecture and training details, consult the https://github.com/opendatalab/DocLayout-YOLO.
