import base64
from io import BytesIO
from pathlib import Path
from typing import List, Union

import fitz
import numpy as np
from PIL import Image


def pdf_to_images(pdf_path: Union[str, Path], dpi: int = 300) -> List[Image.Image]:
    """
    Convert PDF pages to PIL Images.

    Args:
        pdf_path: Path to the PDF file
        dpi: Resolution for the converted images (default: 300)

    Returns:
        List of PIL Image objects, one for each page
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pdf_document = fitz.open(pdf_path)
    images = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        # Get the page's pixmap at specified DPI
        zoom = dpi / 72  # Convert DPI to zoom factor
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=matrix)

        # Convert pixmap to PIL Image
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        images.append(image)

    pdf_document.close()
    return images


def image_to_base64(image: Image.Image) -> str:
    """
    Convert a PIL Image to a base64 encoded string.

    Args:
        image: PIL Image object

    Returns:
        Base64 encoded string
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_str}"
