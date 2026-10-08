import os
import re
from pathlib import Path
from PIL import Image
import pymupdf as fitz  # PyMuPDF

def is_pdf(file_path: str) -> bool:
    """Check if file is a PDF by extension or magic header bytes."""
    if file_path.lower().endswith(".pdf"):
        return True
    try:
        with open(file_path, "rb") as f:
            header = f.read(4)
            return header == b"%PDF"
    except Exception:
        return False

def convert_pdf_page_to_image(pdf_path: str, output_image_path: str, page_num: int = 0) -> str:
    """Render specified single PDF page to a high quality JPEG/PNG image."""
    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            raise ValueError("Uploaded PDF file is empty.")
        
        page = doc.load_page(min(page_num, len(doc) - 1))
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(output_image_path)
        doc.close()
        return output_image_path
    except Exception as e:
        print(f"PyMuPDF single page error: {e}. Trying pypdfium2 fallback.")
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_path)
        page = pdf[page_num]
        image = page.render(scale=2).to_pil()
        image.save(output_image_path)
        return output_image_path

def convert_all_pdf_pages_to_images(pdf_path: str, output_dir: Path, base_prefix: str) -> list:
    """
    Renders ALL pages of a multi-page PDF catalog into individual high-resolution design image files.
    Returns list of dicts: [{'page_num': 1, 'image_path': '...', 'design_code': '...'}, ...]
    """
    results = []
    try:
        doc = fitz.open(pdf_path)
        print(f"Processing multi-page PDF catalog with {len(doc)} pages...")

        for idx, page in enumerate(doc):
            page_num = idx + 1
            text = page.get_text()
            
            # Extract design code from page text if present (e.g., JC4496, SVC 6811, BH325, ANGEL 1511)
            code_match = re.search(r'([A-Z]{2,5}\s*[-_]?\s*\d{3,5})', text)
            if code_match:
                extracted_code = code_match.group(1).replace(" ", "-").upper()
            else:
                extracted_code = f"{base_prefix}-P{page_num}"

            filename = f"{extracted_code}_{page_num}.jpg"
            img_path = output_dir / filename

            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(str(img_path))

            results.append({
                "page_num": page_num,
                "image_path": str(img_path),
                "filename": filename,
                "design_code": extracted_code,
                "text_content": text.strip()
            })

        doc.close()
        return results

    except Exception as e:
        print(f"Error processing multi-page PDF with PyMuPDF: {e}. Trying pypdfium2 fallback.")
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_path)
        for idx, page in enumerate(pdf):
            page_num = idx + 1
            filename = f"{base_prefix}-P{page_num}.jpg"
            img_path = output_dir / filename
            image = page.render(scale=2).to_pil()
            image.save(str(img_path))
            results.append({
                "page_num": page_num,
                "image_path": str(img_path),
                "filename": filename,
                "design_code": f"{base_prefix}-P{page_num}",
                "text_content": ""
            })
        return results

def prepare_image_for_analysis(file_path: str, output_image_path: str) -> str:
    """Ensures a valid RGB image file is available for visual analysis."""
    if is_pdf(file_path):
        return convert_pdf_page_to_image(file_path, output_image_path, page_num=0)
    
    img = Image.open(file_path).convert("RGB")
    img.save(output_image_path, "JPEG", quality=95)
    return output_image_path
