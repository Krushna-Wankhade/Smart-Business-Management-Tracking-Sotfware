# Receipt Processing Feature - Setup & Installation Guide

## Quick Start

### 1. Install Required Python Packages

```bash
pip install pillow pytesseract opencv-python pdf2image
```

### 2. Install Tesseract OCR

#### Windows:
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default path: `C:\Program Files\Tesseract-OCR`)
3. Update path in `receipt_processor.py` if using non-default location:
   ```python
   import pytesseract
   pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### macOS:
```bash
brew install tesseract
```

### 3. Setup Database

Run the database creation script:
```bash
python create_db.py
```

This creates all required tables including:
- `receipt_logs` - Receipt metadata
- `receipt_items` - Individual items
- `transaction_logs` - Audit trail

### 4. Run the Application

```bash
python dashboard.py
```

### 5. Access Receipt Processing

In the main dashboard:
1. Click "Receipt" button in left menu
2. Select receipt image or PDF
3. Click "Process Receipt"
4. View results and history

## File Structure

```
Inventory-Management-System-main/
├── dashboard.py                          # Main application (now with Receipt button)
├── create_db.py                         # Database initialization (updated)
├── receipt_processor.py                 # OCR & NLP engine (NEW)
├── receipt_handler.py                   # Workflow & DB operations (NEW)
├── receipt_ui.py                        # Tkinter UI (NEW)
├── RECEIPT_PROCESSING_GUIDE.md         # Full documentation (NEW)
├── RECEIPT_SETUP_GUIDE.md              # This file
├── employee.py
├── supplier.py
├── category.py
├── product.py
├── sales.py
├── billing.py
├── images/
│   ├── menu_im.png
│   ├── side.png
│   └── ...
├── bill/                                # Sales receipts storage
└── ims.db                              # SQLite database
```

## Key Features

✅ **OCR Text Extraction**
- Automatic text extraction from images and PDFs
- Image preprocessing for better accuracy
- Support for multiple file formats

✅ **Intelligent Parsing**
- NLP-based item extraction (name, quantity, price)
- Automatic receipt type detection (purchase/sales)
- Total amount calculation

✅ **Inventory Management**
- Automatic product lookup in database
- Inventory updates (add/subtract based on receipt type)
- Stock validation (ensures sufficient inventory for sales)

✅ **Complete Audit Trail**
- Receipt logs with metadata
- Item-level details
- Transaction history with old/new quantities

✅ **User-Friendly Interface**
- Simple file upload
- Clear processing results
- Receipt history table
- Error reporting

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB minimum
- **OS**: Windows, Linux, or macOS

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Pillow | Latest | Image processing |
| pytesseract | Latest | OCR interface |
| opencv-python | Latest | Image preprocessing |
| pdf2image | Latest | PDF to image conversion |
| tkinter | Built-in | GUI (included with Python) |
| sqlite3 | Built-in | Database |

## Configuration

### Tesseract Path Configuration (if needed)

Edit the beginning of `receipt_processor.py`:
```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# or
pytesseract.pytesseract.pytesseract_cmd = '/usr/bin/tesseract'  # Linux
```

### Regex Pattern Customization

For different receipt formats, modify the pattern in `receipt_handler.py`:
```python
def parse_receipt_items(self, text):
    item_pattern = r'([a-zA-Z\s]+?)\s+(\d+)\s+([\d.]+)'  # Customize this
```

## Testing the Installation

### Test OCR:
```python
from receipt_processor import ReceiptProcessor

processor = ReceiptProcessor()
text = processor.extract_text_from_image('path/to/image.png')
print(text)
```

### Test Workflow:
```python
from receipt_handler import ReceiptHandler

handler = ReceiptHandler()
result = handler.process_receipt_workflow('path/to/receipt.jpg')
print(result)
```

### Test UI:
```bash
python dashboard.py
# Click Receipt button to test UI
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pytesseract'"
**Solution**: `pip install pytesseract`

### Issue: "TesseractNotFoundError"
**Solution**: 
1. Install Tesseract OCR (see Installation section)
2. Update pytesseract path in `receipt_processor.py`

### Issue: "No module named 'cv2'"
**Solution**: `pip install opencv-python`

### Issue: "ImportError: cannot import name pdf2image"
**Solution**: `pip install pdf2image`

### Issue: Receipt not being recognized
**Solution**:
1. Ensure receipt image is clear and well-lit
2. Check if text is visible in the image
3. Adjust regex pattern if receipt format is non-standard

### Issue: Products not matching
**Solution**:
1. Verify product names match inventory exactly
2. Check for typos in receipt
3. Add missing products to inventory

### Issue: Insufficient stock error
**Solution**:
1. Check current product quantity
2. Adjust sale quantity or purchase stock first
3. Review transaction logs for recent changes

## Performance Optimization

### For Large Batches:
- Process receipts during off-peak hours
- Implement batch processing with progress tracking
- Consider multi-threading for OCR extraction

### For Better Accuracy:
- Use higher resolution receipt images (300+ DPI)
- Ensure well-lit, non-blurry photos
- Standardize receipt format with suppliers

## Monitoring & Maintenance

### Regular Tasks:
1. **Weekly**: Review failed receipts and update patterns
2. **Monthly**: Analyze processing success rates
3. **Quarterly**: Backup database

### Logs to Monitor:
- Receipt processing success/failure rates
- Failed product matches
- Stock shortage incidents
- OCR accuracy metrics

## Support & Documentation

- See `RECEIPT_PROCESSING_GUIDE.md` for detailed documentation
- Check `receipt_processor.py` for OCR/NLP logic
- Review `receipt_handler.py` for database operations
- Inspect `receipt_ui.py` for UI customization

## Next Steps

1. ✅ Install dependencies
2. ✅ Install Tesseract OCR
3. ✅ Run `create_db.py`
4. ✅ Test with sample receipt
5. ✅ Integrate into workflow

---

**Happy Receipt Processing!** 📄✨
