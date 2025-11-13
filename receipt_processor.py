"""
Receipt Processor Module
Handles OCR extraction and NLP parsing of receipt data from images/PDFs
"""

import re
from PIL import Image
from datetime import datetime
import json

# Try to import optional dependencies
try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    print("Warning: pytesseract not available. Manual entry will be used.")

try:
    import pdf2image
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False
    print("Warning: pdf2image not available. PDF processing disabled.")


class ReceiptProcessor:
    def __init__(self):
        """Initialize the Receipt Processor with OCR and NLP capabilities"""
        self.receipt_data = {
            'items': [],
            'total_amount': 0,
            'receipt_type': None,
            'extracted_text': ''
        }
    
    def extract_text_from_image(self, image_path):
        """
        Extract text from image using Tesseract OCR (if available)
        Falls back to manual entry if OCR not available
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text string or empty string if not available
        """
        try:
            if not HAS_TESSERACT:
                print(f"Note: Tesseract not installed. Please enter items manually for {image_path}")
                return ""
            
            # Open image
            image = Image.open(image_path)
            
            # Convert to grayscale for better OCR
            image = image.convert('L')
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)
            self.receipt_data['extracted_text'] = extracted_text
            
            return extracted_text
        except Exception as e:
            print(f"Error extracting text from image: {str(e)}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF using pdf2image and OCR
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text string
        """
        try:
            if not HAS_PDF2IMAGE:
                print("Note: pdf2image not available. Please enter items manually.")
                return ""
            
            if not HAS_TESSERACT:
                print("Note: Tesseract not installed. Please enter items manually.")
                return ""
            
            # Convert PDF to images
            images = pdf2image.convert_from_path(pdf_path)
            extracted_text = ""
            
            for image in images:
                # Convert PIL image to grayscale
                image = image.convert('L')
                
                # Extract text
                text = pytesseract.image_to_string(image)
                extracted_text += text + "\n"
            
            self.receipt_data['extracted_text'] = extracted_text
            return extracted_text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def parse_receipt_items(self, text):
        """
        Parse extracted text to identify items, quantities, and prices using NLP patterns
        
        Args:
            text: Raw extracted text from receipt
            
        Returns:
            List of parsed items with structure: {'name': str, 'qty': int, 'price': float}
        """
        items = []
        lines = text.split('\n')
        
        # Pattern to match: Item Name [Qty] [Price]
        # Supports variations like: "Product 10 500", "Item: 5 qty 250.50"
        item_pattern = r'([a-zA-Z\s]+?)\s+(\d+)\s+([\d.]+)'
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue
            
            # Try to match item pattern
            match = re.search(item_pattern, line)
            if match:
                item_name = match.group(1).strip()
                quantity = int(match.group(2))
                price = float(match.group(3))
                
                # Validate data
                if item_name and quantity > 0 and price > 0:
                    items.append({
                        'name': item_name,
                        'qty': quantity,
                        'price': price
                    })
        
        self.receipt_data['items'] = items
        return items
    
    def detect_receipt_type(self, text):
        """
        Detect if receipt is for Purchase (stock addition) or Sales (stock deduction)
        
        Args:
            text: Extracted receipt text
            
        Returns:
            'purchase' or 'sales'
        """
        text_lower = text.lower()
        
        # Keywords for purchase receipts
        purchase_keywords = ['purchase', 'invoice', 'supplier', 'bill', 'order', 'wholesale', 'received']
        
        # Keywords for sales receipts
        sales_keywords = ['sale', 'receipt', 'customer', 'sold', 'invoice #', 'retail', 'bill to']
        
        purchase_count = sum(1 for keyword in purchase_keywords if keyword in text_lower)
        sales_count = sum(1 for keyword in sales_keywords if keyword in text_lower)
        
        receipt_type = 'purchase' if purchase_count >= sales_count else 'sales'
        self.receipt_data['receipt_type'] = receipt_type
        
        return receipt_type
    
    def calculate_total(self):
        """
        Calculate total amount from parsed items
        
        Returns:
            Total amount as float
        """
        total = sum(item['qty'] * item['price'] for item in self.receipt_data['items'])
        self.receipt_data['total_amount'] = total
        return total
    
    def process_receipt(self, file_path, manual_items=None):
        """
        Complete workflow: Read file → Extract text → Parse items → Detect type → Calculate total
        
        Args:
            file_path: Path to image or PDF file
            manual_items: Optional list of manually entered items for fallback
            
        Returns:
            Dictionary with processed receipt data
        """
        # Determine file type
        file_ext = file_path.lower().split('.')[-1]
        
        # Extract text based on file type
        if file_ext == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_image(file_path)
        
        # If OCR didn't extract text but manual items provided, use them
        if not text and manual_items:
            self.receipt_data['items'] = manual_items
            self.receipt_data['total_amount'] = self.calculate_total()
            self.detect_receipt_type("manual entry")
            return self.receipt_data
        
        if not text:
            # If no text extracted and no manual items, return empty
            return self.receipt_data
        
        # Parse items from text
        self.parse_receipt_items(text)
        
        # Detect receipt type
        self.detect_receipt_type(text)
        
        # Calculate total
        self.calculate_total()
        
        return self.receipt_data
    
    def get_processed_data(self):
        """Return the processed receipt data"""
        return self.receipt_data
    
    def reset(self):
        """Reset receipt data for processing new receipt"""
        self.receipt_data = {
            'items': [],
            'total_amount': 0,
            'receipt_type': None,
            'extracted_text': ''
        }
    
    def add_manual_item(self, name, qty, price):
        """
        Manually add an item to the receipt
        
        Args:
            name: Product name
            qty: Quantity
            price: Unit price
            
        Returns:
            Updated items list
        """
        if name and qty > 0 and price > 0:
            self.receipt_data['items'].append({
                'name': name,
                'qty': qty,
                'price': price
            })
            self.calculate_total()
            return True
        return False
    
    def remove_item(self, index):
        """
        Remove an item from the receipt by index
        
        Args:
            index: Index of item to remove
            
        Returns:
            Updated items list
        """
        if 0 <= index < len(self.receipt_data['items']):
            self.receipt_data['items'].pop(index)
            self.calculate_total()
            return True
        return False
