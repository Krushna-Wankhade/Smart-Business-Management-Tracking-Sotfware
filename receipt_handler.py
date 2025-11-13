"""
Receipt Handler Module
Manages receipt workflow - validates products, updates inventory, logs transactions
"""

import sqlite3
from datetime import datetime
from receipt_processor import ReceiptProcessor

class ReceiptHandler:
    def __init__(self, db_path='ims.db'):
        """
        Initialize Receipt Handler
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        self.processor = ReceiptProcessor()
    
    def get_product_by_name(self, product_name):
        """
        Search for product in database by name
        
        Args:
            product_name: Name of the product
            
        Returns:
            Product tuple (pid, Category, Supplier, name, price, qty, status) or None
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            # Search for product with similar name
            cur.execute(
                "SELECT * FROM product WHERE name LIKE ?",
                (f"%{product_name}%",)
            )
            result = cur.fetchone()
            con.close()
            
            return result
        except Exception as e:
            print(f"Error fetching product: {str(e)}")
            return None
    
    def update_product_quantity(self, product_id, quantity_change, action='add'):
        """
        Update product quantity in inventory
        
        Args:
            product_id: ID of the product
            quantity_change: Amount to add or subtract
            action: 'add' for purchase or 'subtract' for sales
            
        Returns:
            Tuple of (success: bool, old_qty: int, new_qty: int, message: str)
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            # Get current quantity
            cur.execute("SELECT qty FROM product WHERE pid=?", (product_id,))
            result = cur.fetchone()
            
            if not result:
                return (False, 0, 0, "Product not found")
            
            old_qty = int(result[0])
            
            # Calculate new quantity
            if action == 'add':
                new_qty = old_qty + quantity_change
            else:  # subtract
                if old_qty < quantity_change:
                    con.close()
                    return (False, old_qty, 0, f"Insufficient stock. Available: {old_qty}, Required: {quantity_change}")
                new_qty = old_qty - quantity_change
            
            # Update quantity
            cur.execute(
                "UPDATE product SET qty=? WHERE pid=?",
                (new_qty, product_id)
            )
            con.commit()
            con.close()
            
            return (True, old_qty, new_qty, "Quantity updated successfully")
        
        except Exception as e:
            return (False, 0, 0, f"Error updating quantity: {str(e)}")
    
    def save_receipt_log(self, receipt_type, file_name, total_items, total_amount):
        """
        Save receipt log to database
        
        Args:
            receipt_type: 'purchase' or 'sales'
            file_name: Original file name
            total_items: Number of items in receipt
            total_amount: Total amount
            
        Returns:
            receipt_id or None
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cur.execute(
                """INSERT INTO receipt_logs 
                (receipt_type, upload_date, file_name, total_items, total_amount, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (receipt_type, upload_date, file_name, total_items, total_amount, 'completed', 'Auto-processed')
            )
            con.commit()
            receipt_id = cur.lastrowid
            con.close()
            
            return receipt_id
        
        except Exception as e:
            print(f"Error saving receipt log: {str(e)}")
            return None
    
    def save_receipt_items(self, receipt_id, items_data):
        """
        Save individual receipt items
        
        Args:
            receipt_id: ID of the receipt
            items_data: List of dicts with item info
            
        Returns:
            List of saved item IDs
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            item_ids = []
            
            for item in items_data:
                cur.execute(
                    """INSERT INTO receipt_items
                    (receipt_id, product_id, product_name, quantity, unit_price, total_price, action)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        receipt_id,
                        item.get('product_id'),
                        item.get('product_name'),
                        item.get('quantity'),
                        item.get('unit_price'),
                        item.get('total_price'),
                        item.get('action')
                    )
                )
                item_ids.append(cur.lastrowid)
            
            con.commit()
            con.close()
            
            return item_ids
        
        except Exception as e:
            print(f"Error saving receipt items: {str(e)}")
            return []
    
    def save_transaction_log(self, receipt_id, product_id, product_name, quantity, action, old_qty, new_qty):
        """
        Save transaction log for audit trail
        
        Args:
            receipt_id: ID of the receipt
            product_id: ID of the product
            product_name: Name of the product
            quantity: Quantity changed
            action: 'add' or 'subtract'
            old_qty: Previous quantity
            new_qty: New quantity
            
        Returns:
            transaction_id or None
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cur.execute(
                """INSERT INTO transaction_logs
                (receipt_id, product_id, product_name, quantity, action, old_qty, new_qty, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (receipt_id, product_id, product_name, quantity, action, old_qty, new_qty, timestamp)
            )
            con.commit()
            txn_id = cur.lastrowid
            con.close()
            
            return txn_id
        
        except Exception as e:
            print(f"Error saving transaction log: {str(e)}")
            return None
    
    def process_receipt_workflow(self, file_path, manual_items=None, receipt_type_override=None):
        """
        Complete workflow: Extract → Parse → Match products → Update inventory → Log
        
        Args:
            file_path: Path to receipt file (image/PDF) or temporary name for manual entry
            manual_items: Optional list of manually entered items
            receipt_type_override: Override receipt type detection
            
        Returns:
            Dict with processing results
        """
        result = {
            'success': False,
            'receipt_id': None,
            'processed_items': [],
            'failed_items': [],
            'message': ''
        }
        
        try:
            # Step 1: Process receipt (OCR + NLP or use manual items)
            self.processor.reset()
            
            if manual_items:
                # Use manually entered items
                receipt_data = {
                    'items': manual_items,
                    'receipt_type': receipt_type_override or 'purchase',
                    'extracted_text': 'Manual Entry',
                    'total_amount': sum(item['qty'] * item['price'] for item in manual_items)
                }
            else:
                receipt_data = self.processor.process_receipt(file_path)
            
            if not receipt_data or not receipt_data['items']:
                result['message'] = 'No items found in receipt. Please add items manually.'
                return result
            
            # Step 2: Save receipt log
            receipt_id = self.save_receipt_log(
                receipt_data['receipt_type'],
                file_path.split('\\')[-1] if '\\' in file_path else file_path,
                len(receipt_data['items']),
                receipt_data['total_amount']
            )
            
            if not receipt_id:
                result['message'] = 'Failed to save receipt log'
                return result
            
            result['receipt_id'] = receipt_id
            
            # Step 3: Process each item
            for item in receipt_data['items']:
                # Find matching product
                product = self.get_product_by_name(item['name'])
                
                if not product:
                    result['failed_items'].append({
                        'name': item['name'],
                        'reason': 'Product not found in inventory'
                    })
                    continue
                
                product_id = product[0]
                
                # Determine action based on receipt type
                action = 'add' if receipt_data['receipt_type'] == 'purchase' else 'subtract'
                
                # Update inventory
                success, old_qty, new_qty, msg = self.update_product_quantity(
                    product_id,
                    item['qty'],
                    action
                )
                
                if not success:
                    result['failed_items'].append({
                        'name': item['name'],
                        'reason': msg
                    })
                    continue
                
                # Save receipt item
                item_data = {
                    'product_id': product_id,
                    'product_name': item['name'],
                    'quantity': item['qty'],
                    'unit_price': item['price'],
                    'total_price': item['qty'] * item['price'],
                    'action': action
                }
                self.save_receipt_items(receipt_id, [item_data])
                
                # Save transaction log
                self.save_transaction_log(
                    receipt_id, product_id, item['name'],
                    item['qty'], action, old_qty, new_qty
                )
                
                result['processed_items'].append({
                    'name': item['name'],
                    'qty': item['qty'],
                    'old_qty': old_qty,
                    'new_qty': new_qty,
                    'action': action
                })
            
            result['success'] = True
            result['message'] = f"Receipt processed: {len(result['processed_items'])} items updated"
            
        except Exception as e:
            result['message'] = f"Error processing receipt: {str(e)}"
        
        return result
    
    def get_receipt_history(self, limit=10):
        """
        Get recent receipt history
        
        Args:
            limit: Number of recent receipts to fetch
            
        Returns:
            List of receipt records
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            cur.execute(
                """SELECT * FROM receipt_logs 
                ORDER BY receipt_id DESC LIMIT ?""",
                (limit,)
            )
            results = cur.fetchall()
            con.close()
            
            return results
        
        except Exception as e:
            print(f"Error fetching receipt history: {str(e)}")
            return []
    
    def get_receipt_details(self, receipt_id):
        """
        Get detailed information about a specific receipt
        
        Args:
            receipt_id: ID of the receipt
            
        Returns:
            Dict with receipt and items details
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            # Get receipt log
            cur.execute("SELECT * FROM receipt_logs WHERE receipt_id=?", (receipt_id,))
            receipt = cur.fetchone()
            
            # Get receipt items
            cur.execute("SELECT * FROM receipt_items WHERE receipt_id=?", (receipt_id,))
            items = cur.fetchall()
            
            # Get transaction logs
            cur.execute("SELECT * FROM transaction_logs WHERE receipt_id=?", (receipt_id,))
            transactions = cur.fetchall()
            
            con.close()
            
            return {
                'receipt': receipt,
                'items': items,
                'transactions': transactions
            }
        
        except Exception as e:
            print(f"Error fetching receipt details: {str(e)}")
            return None
