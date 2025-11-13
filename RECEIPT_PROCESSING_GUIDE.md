# Receipt Processing & Inventory Update Workflow

## Overview
The Receipt Processing feature enables automatic extraction of receipt data from images (PNG, JPG, BMP) and PDFs, intelligent parsing of item information, and automatic inventory updates with full transaction tracking.

## Workflow Steps

### Step 1: Upload or Capture Receipt
- **Action**: User uploads receipt image or PDF file
- **Supported Formats**:
  - Images: PNG, JPG, JPEG, BMP
  - Documents: PDF
- **Location**: Via "Receipt" menu in main dashboard

### Step 2: OCR Text Extraction
- **Engine**: Tesseract OCR
- **Process**:
  - Image preprocessing (grayscale conversion, thresholding, denoising)
  - Optical Character Recognition to extract text
  - Support for both image and PDF processing
- **Output**: Raw extracted text from receipt

### Step 3: NLP Parsing & Data Extraction
- **Parser**: Regular Expression-based NLP parser
- **Extracts**:
  - Item names
  - Quantities
  - Unit prices
  - Total prices
- **Pattern Matching**: Supports various receipt formats
  - Format: "Item Name [Quantity] [Price]"
  - Examples: "Product 10 500", "Item: 5 qty 250.50"

### Step 4: Product Matching & Verification
- **Process**:
  - Search database for matching product by name
  - Supports partial name matching (LIKE query)
  - Returns product ID and current stock quantity
- **Validation**:
  - Verifies product exists in inventory
  - Flags unmatched items for manual review

### Step 5: Inventory Update
- **Purchase Receipt** → ADD stock quantities
  - New Qty = Current Qty + Purchase Qty
  - Use case: When receiving stock from suppliers
  
- **Sales Receipt** → DEDUCT stock quantities
  - New Qty = Current Qty - Sale Qty
  - Validates sufficient stock available
  - Use case: When selling to customers

### Step 6: Transaction Logging
- **Saved Information**:
  - Receipt metadata (type, upload date, file name, total items, amount)
  - Individual receipt items (product name, qty, price, action)
  - Transaction logs (product changes, old/new quantities, timestamp)
- **Purpose**:
  - Complete audit trail
  - Historical reporting
  - Inventory tracking
  - Reconciliation

## Database Schema

### receipt_logs Table
```sql
CREATE TABLE receipt_logs (
    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_type TEXT,           -- 'purchase' or 'sales'
    upload_date TEXT,             -- Timestamp of upload
    file_name TEXT,               -- Original file name
    total_items INTEGER,          -- Number of items in receipt
    total_amount REAL,            -- Total transaction amount
    status TEXT,                  -- Processing status
    notes TEXT                     -- Additional notes
)
```

### receipt_items Table
```sql
CREATE TABLE receipt_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER,           -- Foreign key to receipt_logs
    product_id INTEGER,           -- Foreign key to product
    product_name TEXT,            -- Product name
    quantity INTEGER,             -- Quantity in this receipt
    unit_price REAL,              -- Price per unit
    total_price REAL,             -- Quantity * Unit Price
    action TEXT,                  -- 'add' or 'subtract'
    FOREIGN KEY(receipt_id) REFERENCES receipt_logs(receipt_id),
    FOREIGN KEY(product_id) REFERENCES product(pid)
)
```

### transaction_logs Table
```sql
CREATE TABLE transaction_logs (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER,           -- Foreign key to receipt_logs
    product_id INTEGER,           -- Foreign key to product
    product_name TEXT,            -- Product name
    quantity INTEGER,             -- Quantity changed
    action TEXT,                  -- 'add' or 'subtract'
    old_qty INTEGER,              -- Stock before transaction
    new_qty INTEGER,              -- Stock after transaction
    timestamp TEXT,               -- Transaction time
    FOREIGN KEY(receipt_id) REFERENCES receipt_logs(receipt_id),
    FOREIGN KEY(product_id) REFERENCES product(pid)
)
```

## Module Architecture

### 1. receipt_processor.py
**Responsibilities**: OCR and NLP Processing

**Key Classes**:
- `ReceiptProcessor`: Main processing engine

**Key Methods**:
- `extract_text_from_image(image_path)`: Tesseract OCR for images
- `extract_text_from_pdf(pdf_path)`: PDF to image conversion + OCR
- `parse_receipt_items(text)`: NLP parsing using regex patterns
- `detect_receipt_type(text)`: Classify as purchase or sales
- `calculate_total()`: Sum item amounts
- `process_receipt(file_path)`: Complete workflow pipeline
- `get_processed_data()`: Return processed data
- `reset()`: Clear data for new receipt

**Dependencies**:
- cv2 (OpenCV) - Image processing
- pytesseract - OCR wrapper
- pdf2image - PDF conversion
- PIL (Pillow) - Image handling
- re - Regular expressions
- datetime - Timestamps

### 2. receipt_handler.py
**Responsibilities**: Workflow Management & Database Operations

**Key Classes**:
- `ReceiptHandler`: Orchestrates receipt processing workflow

**Key Methods**:
- `get_product_by_name(product_name)`: Product lookup
- `update_product_quantity(product_id, quantity_change, action)`: Inventory update
- `save_receipt_log()`: Store receipt metadata
- `save_receipt_items()`: Store receipt items
- `save_transaction_log()`: Store transaction audit trail
- `process_receipt_workflow(file_path)`: Complete end-to-end processing
- `get_receipt_history(limit)`: Fetch recent receipts
- `get_receipt_details(receipt_id)`: Get specific receipt with items

**Dependencies**:
- sqlite3 - Database
- datetime - Timestamps
- receipt_processor - OCR/NLP engine

### 3. receipt_ui.py
**Responsibilities**: User Interface & Result Display

**Key Classes**:
- `ReceiptProcessingUI`: Tkinter UI component
- `open_receipt_window(parent_root)`: Factory function

**Key Features**:
- File upload dialog
- Receipt selection display
- Processing status display
- Results visualization
- Receipt history table
- Transaction details

**UI Components**:
- File selection button
- Process receipt button
- Results text area (scrollable)
- Receipt history table (recent 10 receipts)

**Dependencies**:
- tkinter - GUI
- PIL - Image display
- receipt_handler - Core logic
- datetime - Timestamps

## Usage Instructions

### For End Users

1. **Open Receipt Processing Window**:
   - Click "Receipt" button in main dashboard menu

2. **Upload Receipt**:
   - Click "📁 Select Receipt File" button
   - Choose image (PNG/JPG) or PDF file
   - Selected file name appears with checkmark

3. **Process Receipt**:
   - Click "⚙️ Process Receipt" button
   - Wait for processing to complete
   - Success/error message displayed

4. **Review Results**:
   - View processed items in results panel
   - Check if all items matched successfully
   - Review failed items and reasons
   - Note quantity changes (Old Qty → New Qty)

5. **View History**:
   - Recent receipts displayed in bottom table
   - Shows Receipt ID, Type, Date, Items, Amount, Status
   - Click to view detailed receipt information

### For Developers

#### Installation of Dependencies
```bash
pip install pillow pytesseract opencv-python pdf2image
```

#### Tesseract Installation
- **Windows**: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

#### Custom Receipt Patterns
Edit `parse_receipt_items()` regex pattern in `receipt_processor.py`:
```python
item_pattern = r'([a-zA-Z\s]+?)\s+(\d+)\s+([\d.]+)'
```

#### Testing
```python
from receipt_handler import ReceiptHandler

handler = ReceiptHandler()
result = handler.process_receipt_workflow('path/to/receipt.jpg')
print(result)
```

## Error Handling

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No file selected" | User didn't select file | Click file selection button |
| "No items found in receipt" | Poor image quality or non-receipt image | Ensure clear, well-lit receipt image |
| "Product not found" | Item name doesn't match database | Add product to inventory or correct receipt |
| "Insufficient stock" | Sales qty > available stock | Adjust sale quantity |
| "Failed to extract text" | Tesseract not installed | Install Tesseract OCR |

### Receipt Quality Requirements
- **Minimum Resolution**: 300 DPI
- **Format**: Clear, well-lit images
- **Content**: Items, quantities, prices visible
- **Orientation**: Upright, not rotated

## Performance Metrics

| Operation | Typical Time |
|-----------|--------------|
| OCR extraction (single page) | 2-5 seconds |
| NLP parsing | <1 second |
| Database lookup | <0.5 seconds |
| Inventory update | <0.5 seconds |
| Complete workflow | 3-7 seconds |

## Future Enhancements

1. **Machine Learning**:
   - Improved item classification using ML models
   - Automatic receipt type detection accuracy
   - Price prediction and validation

2. **Advanced OCR**:
   - Handwritten text support
   - Multi-language recognition
   - Receipt template detection

3. **Integration**:
   - Email receipt import
   - Supplier receipt auto-matching
   - Barcode/QR code scanning

4. **Analytics**:
   - Receipt processing analytics
   - Supplier performance tracking
   - Sales trend analysis

5. **Batch Processing**:
   - Process multiple receipts at once
   - Scheduled batch uploads
   - Automated reconciliation

## Troubleshooting Guide

### Tesseract Not Found
```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### PDF Processing Fails
- Ensure pdf2image is installed: `pip install pdf2image`
- Install system PDF tools: `pip install pdf2image[wand]`

### Low OCR Accuracy
- Improve image quality (higher DPI, better lighting)
- Use better image preprocessing (adjust thresholds)
- Manually correct items not recognized

### Database Errors
- Ensure ims.db exists (run create_db.py)
- Check database permissions
- Verify SQLite3 installation

## Example Receipt Format

```
SUPPLIER INVOICE
Invoice #: 001234
Date: 2025-11-11

ITEMS:
Product A 10 500
Item B 5 250.50
Widget C 20 100

Total Items: 35
Total Amount: 8,250.00

Status: Received
```

## Compliance & Security

- **Data Privacy**: All receipt data stored locally in SQLite
- **Audit Trail**: Complete transaction history maintained
- **Access Control**: Integrated with employee authentication
- **Data Validation**: Input sanitization and format validation
- **Backup**: Regular database backups recommended

---

**Version**: 1.0  
**Last Updated**: November 11, 2025  
**Status**: Production Ready
