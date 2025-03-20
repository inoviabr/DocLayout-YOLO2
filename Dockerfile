FROM nvcr.io/nvidia/pytorch:23.10-py3

# 1. Setting up the environment
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

# 2. System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libgl1 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 3. Setting up a working directory
WORKDIR /app

# 4. Copy and install requirements
COPY requirements.txt .
RUN sed -i '/opencv-python/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir py-cpuinfo



# 5. Copy project
COPY . .



# 6. Entry point
CMD ["python", "pipeline.py", \
    "--pdf_folder", "/app/input_pdfs", \
    "--output_folder", "/app/results", \
    "--ocr_lang", "por"]
