Segue o conteúdo do README.md atualizado com as instruções de uso do Docker. Basta copiar e colar o conteúdo no VSCode:

```markdown
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

## Running with Docker

This project supports Docker for easy deployment and execution. Follow the instructions below to build and run the container on your machine.

### Prerequisites
Ensure that Docker and Docker Compose are installed. Verify your installations with:

```bash
docker --version
docker-compose --version
```

### Building the Docker Image
To build the Docker image without using cache, run:

```bash
docker-compose build --no-cache
```

### Running the Docker Container
To run the container, set the environment variables for your input and output directories and then execute:

```bash
INPUT_PDFS="/path/to/input_pdfs" OUTPUT_FOLDER="/path/to/output" docker-compose up
```

Replace `/path/to/input_pdfs` and `/path/to/output` with the correct paths on your machine.

### Stopping the Container
To stop the container, execute:

```bash
docker-compose down
```

### Viewing Logs
For monitoring logs in real time, use:

```bash
docker-compose logs -f
```

## Documentation
For original model architecture and training details, consult the [DocLayout-YOLO repository](https://github.com/opendatalab/DocLayout-YOLO).
```

Essa versão já está pronta para ser utilizada no VSCode. Caso necessite de mais alguma alteração, estou à disposição!