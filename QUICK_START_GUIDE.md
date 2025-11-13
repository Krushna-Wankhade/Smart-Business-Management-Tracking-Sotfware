# 🚀 Quick Start Guide - Receipt Processing

## Get Started in 30 Seconds

### 1️⃣ Start the Application
```bash
python dashboard.py
```

### 2️⃣ Click "Receipt" Button
- Located in the left menu of main dashboard

### 3️⃣ Choose Your Method

#### Method A: Upload Receipt Image (with OCR)
```
1. Click "Upload Receipt" tab
2. Click "📁 Select Receipt File"
3. Choose image (PNG/JPG) or PDF
4. Click "⚙️ Process Receipt"
5. View results
```

#### Method B: Manual Entry (RECOMMENDED ⭐)
```
1. Click "Manual Entry" tab
2. Enter Product Name (from inventory)
3. Enter Quantity
4. Enter Unit Price
5. Select Receipt Type: Purchase or Sales
6. Click "➕ Add Item" for more items
7. Click "✔️ Process Receipt"
```

#### Method C: View History
```
1. Click "History" tab
2. See all processed receipts
3. Click "🔄 Refresh" to reload
```

---

## 📝 Example: Add Items Manually

### Purchase Receipt (Adding Stock)
```
Product Name:  Laptop
Quantity:      10
Unit Price:    ₹50,000
Receipt Type:  Purchase  ← SELECT THIS

✨ Result: Inventory +10 Laptops
```

### Sales Receipt (Selling Items)
```
Product Name:  Mouse
Quantity:      50
Unit Price:    ₹500
Receipt Type:  Sales  ← SELECT THIS

✨ Result: Inventory -50 Mice
```

---

## ✅ Key Points to Remember

1. **Product Names Must Match**: Enter exact product name from inventory
2. **Receipt Type Matters**: 
   - Purchase = Add to stock
   - Sales = Subtract from stock
3. **Stock Validation**: System prevents selling more than available
4. **All Recorded**: Every transaction is logged for audit

---

## ❌ Troubleshooting

### "Product not found in inventory"
→ Check exact product name in inventory
→ Add product first if it doesn't exist

### "Insufficient stock"
→ Current stock is less than sale quantity
→ Purchase more stock first

### "No items found in receipt"
→ Use Manual Entry tab instead
→ Tesseract OCR not installed

### Application won't start
→ Run: `python create_db.py` first
→ Ensure Python 3.8+ installed

---

## 📊 What Happens After Processing

1. ✅ Receipt saved to database
2. ✅ Inventory updated (quantities changed)
3. ✅ Transaction logged (audit trail)
4. ✅ Success message displayed
5. ✅ Receipt ID generated
6. ✅ Visible in History tab

---

## 🎯 Common Workflows

### Workflow 1: Receiving New Stock
```
Type: Purchase
Items: [Product1: 10, Product2: 5, Product3: 20]
→ Inventory increases for all products
```

### Workflow 2: Selling to Customers
```
Type: Sales
Items: [Product1: 2, Product2: 3]
→ Inventory decreases for these products
```

### Workflow 3: Inventory Adjustment
```
Type: Purchase (to add) or Sales (to deduct)
Items: Single item with adjustment quantity
→ Corrects inventory discrepancies
```

---

## 💾 Data Stored

For each receipt:
- Receipt ID (unique number)
- Type (Purchase/Sales)
- Date & Time
- Items (name, qty, price)
- Total Amount
- Status (completed/failed)
- Failed items (if any)

---

## 🔗 Navigation

```
Dashboard
    └─ Receipt Button
        ├─ Upload Receipt Tab
        │   ├─ Select File
        │   ├─ Process Receipt
        │   └─ View Results
        │
        ├─ Manual Entry Tab (⭐ RECOMMENDED)
        │   ├─ Enter Product Name
        │   ├─ Enter Quantity
        │   ├─ Enter Unit Price
        │   ├─ Select Receipt Type
        │   ├─ Add Items to List
        │   └─ Process Receipt
        │
        └─ History Tab
            ├─ View Recent Receipts
            └─ Refresh History
```

---

## ⏱️ Expected Times

| Operation | Time |
|-----------|------|
| Add single item | < 1 second |
| Add 10 items | < 10 seconds |
| Process receipt | 1-3 seconds |
| Update inventory | < 0.5 seconds |
| View history | < 1 second |

---

## 🎓 Tips & Tricks

✅ **Tip 1**: Use manual entry if OCR is not working
✅ **Tip 2**: Add multiple items before processing
✅ **Tip 3**: Check history for past transactions
✅ **Tip 4**: Double-check product names before processing
✅ **Tip 5**: Sales receipts cannot exceed available stock

---

## 📞 Help Resources

- See `RECEIPT_PROCESSING_GUIDE.md` for detailed docs
- See `RECEIPT_SETUP_GUIDE.md` for installation help
- Check source code comments in:
  - `receipt_processor.py` (OCR/NLP logic)
  - `receipt_handler.py` (Database operations)
  - `receipt_ui.py` (User interface)

---

## ✨ Features at a Glance

| Feature | Status | Notes |
|---------|--------|-------|
| File Upload | ✅ | PNG, JPG, PDF |
| Manual Entry | ✅ | **Use this if OCR fails** |
| OCR Processing | ✅ | Optional, requires Tesseract |
| NLP Parsing | ✅ | Automatic item extraction |
| Inventory Update | ✅ | Purchase/Sales both work |
| Stock Validation | ✅ | Prevents overselling |
| Audit Trail | ✅ | Complete transaction logs |
| Receipt History | ✅ | View all past receipts |
| Error Handling | ✅ | Detailed error messages |

---

**Ready to use? Click the Receipt button and get started! 🚀**
