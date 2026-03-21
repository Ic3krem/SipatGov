import logging
from typing import List, Dict
import os
import cv2
import numpy as np
from PIL import Image
from config import PROCESSED_DIR, DEVICE, OCR_MODEL

logger = logging.getLogger(__name__)

class OCRProcessor:
    """OCR processor for scanned PDFs and images"""
    
    def __init__(self):
        self.device = DEVICE
        self.model_type = OCR_MODEL
        self.init_model()
    
    def init_model(self):
        """Initialize OCR model"""
        try:
            if self.model_type == "paddleocr":
                try:
                    from paddleocr import PaddleOCR
                    self.model = PaddleOCR(use_angle_cls=True, lang='en')
                    logger.info("PaddleOCR initialized")
                except ImportError:
                    logger.warning("PaddleOCR not available, falling back to pytesseract")
                    self.model_type = "pytesseract"
            
            if self.model_type == "pytesseract":
                import pytesseract
                self.model = pytesseract
                logger.info("Pytesseract initialized")
        except Exception as e:
            logger.error(f"Error initializing OCR model: {str(e)}")
            self.model = None
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """Extract text from image using OCR"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Cannot read image: {image_path}")
                return {'status': 'failed', 'error': 'Cannot read image'}
            
            if self.model_type == "paddleocr" and self.model:
                result = self.model.ocr(image, cls=True)
                text = '\n'.join([line[1][0] for line in result[0]]) if result else ""
            else:
                # Fallback to Tesseract
                text = self._tesseract_ocr(image)
            
            logger.info(f"Extracted text from {image_path}, length: {len(text)}")
            return {
                'status': 'success',
                'text': text,
                'confidence': self._estimate_confidence(text),
                'source': image_path
            }
        except Exception as e:
            logger.error(f"Error in OCR: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """Extract text from PDF (convert to images first)"""
        try:
            from pdf2image import convert_from_path
            from PyPDF2 import PdfReader
            
            all_text = ""
            
            # Try PDF2Image first for scanned PDFs
            try:
                images = convert_from_path(pdf_path, first_page=1, last_page=3)  # Limit to first 3 pages
                for i, image in enumerate(images):
                    img_array = np.array(image)
                    if self.model_type == "paddleocr" and self.model:
                        result = self.model.ocr(img_array, cls=True)
                        text = '\n'.join([line[1][0] for line in result[0]]) if result else ""
                    else:
                        text = self._tesseract_ocr(img_array)
                    
                    all_text += f"\n--- Page {i+1} ---\n{text}"
            except Exception as e:
                logger.warning(f"PDF2Image failed: {str(e)}, trying PyPDF2")
                # Fallback to PyPDF2 for text PDFs
                pdf_reader = PdfReader(pdf_path)
                for page in pdf_reader.pages[:3]:  # Limit to first 3 pages
                    all_text += page.extract_text()
            
            logger.info(f"Extracted text from PDF {pdf_path}, length: {len(all_text)}")
            return {
                'status': 'success',
                'text': all_text[:5000],  # Limit output
                'confidence': self._estimate_confidence(all_text),
                'source': pdf_path,
                'pages_processed': min(3, len(images) if 'images' in locals() else 1)
            }
        except Exception as e:
            logger.error(f"Error in PDF OCR: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def _tesseract_ocr(self, image) -> str:
        """Fallback OCR using Tesseract"""
        try:
            import pytesseract
            # Preprocess image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            text = pytesseract.image_to_string(processed)
            return text
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {str(e)}")
            return ""
    
    def _estimate_confidence(self, text: str) -> float:
        """Estimate OCR confidence based on text quality"""
        if not text:
            return 0.0
        
        # Simple heuristic: check for readable patterns
        readable_chars = sum(1 for c in text if c.isalnum() or c.isspace())
        confidence = min(1.0, readable_chars / len(text)) if len(text) > 0 else 0.0
        return round(confidence, 2)
    
    def process_batch(self, file_paths: List[str]) -> List[Dict]:
        """Process multiple files"""
        results = []
        for filepath in file_paths:
            if filepath.lower().endswith('.pdf'):
                result = self.extract_text_from_pdf(filepath)
            else:
                result = self.extract_text_from_image(filepath)
            results.append(result)
        
        return results
