"""
Receipt Processing UI Module
Tkinter interface for uploading and processing receipts
"""

from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from datetime import datetime
from receipt_handler import ReceiptHandler

class ReceiptProcessingUI:
    def __init__(self, root):
        """Initialize Receipt Processing UI"""
        self.root = root
        self.root.title("Receipt Processing System")
        self.root.geometry("1200x900")
        self.root.configure(bg='white')
        
        self.handler = ReceiptHandler()
        self.selected_file = None
        self.manual_items = []
        
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface"""
        
        # Header
        header_frame = Frame(self.root, bg="#009688", height=50)
        header_frame.pack(side=TOP, fill=X)
        
        title = Label(
            header_frame,
            text="📄 Receipt Processing & Inventory Update",
            font=("times new roman", 20, "bold"),
            bg="#009688",
            fg="white"
        )
        title.pack(side=LEFT, padx=20, pady=10)
        
        # Main notebook with tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: File Upload
        tab1 = Frame(notebook, bg='white')
        notebook.add(tab1, text="Upload Receipt")
        self.create_upload_tab(tab1)
        
        # Tab 2: Manual Entry
        tab2 = Frame(notebook, bg='white')
        notebook.add(tab2, text="Manual Entry")
        self.create_manual_entry_tab(tab2)
        
        # Tab 3: History
        tab3 = Frame(notebook, bg='white')
        notebook.add(tab3, text="History")
        self.create_history_tab(tab3)
    
    def create_upload_tab(self, parent):
        """Create file upload tab"""
        # Left panel - Upload section
        left_panel = Frame(parent, bg='white')
        left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        
        # Upload section label
        upload_label = Label(
            left_panel,
            text="Step 1: Upload Receipt",
            font=("times new roman", 14, "bold"),
            bg='white'
        )
        upload_label.pack(pady=10)
        
        # File selection area
        file_frame = Frame(left_panel, bg='white', relief=RIDGE, bd=2)
        file_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.file_label = Label(
            file_frame,
            text="No file selected\n(Click below to select image or PDF)",
            font=("times new roman", 12),
            bg='white',
            fg='gray'
        )
        self.file_label.pack(pady=20)
        
        # Buttons
        button_frame = Frame(left_panel, bg='white')
        button_frame.pack(fill=X, padx=10, pady=10)
        
        upload_btn = Button(
            button_frame,
            text="📁 Select Receipt File",
            command=self.select_file,
            font=("times new roman", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            padx=15,
            pady=8
        )
        upload_btn.pack(side=LEFT, padx=5)
        
        process_btn = Button(
            button_frame,
            text="⚙️ Process Receipt",
            command=self.process_receipt,
            font=("times new roman", 11, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            padx=15,
            pady=8
        )
        process_btn.pack(side=LEFT, padx=5)
        
        # Right panel - Results section
        right_panel = Frame(parent, bg='white')
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        
        results_label = Label(
            right_panel,
            text="Processing Results",
            font=("times new roman", 14, "bold"),
            bg='white'
        )
        results_label.pack(pady=10)
        
        # Results frame with scrollbar
        results_frame = Frame(right_panel, bg='white', relief=RIDGE, bd=2)
        results_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = Scrollbar(results_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.results_text = Text(
            results_frame,
            font=("courier", 9),
            yscrollcommand=scrollbar.set,
            height=25,
            width=45
        )
        self.results_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.results_text.yview)
    
    def create_manual_entry_tab(self, parent):
        """Create manual item entry tab"""
        # Left panel - Item entry
        left_panel = Frame(parent, bg='white')
        left_panel.pack(side=LEFT, fill=BOTH, padx=10, pady=10, expand=True)
        
        entry_label = Label(
            left_panel,
            text="Enter Receipt Items Manually",
            font=("times new roman", 14, "bold"),
            bg='white'
        )
        entry_label.pack(pady=10)
        
        # Entry fields frame
        fields_frame = Frame(left_panel, bg='white')
        fields_frame.pack(fill=X, padx=10, pady=10)
        
        # Product name
        Label(fields_frame, text="Product Name:", font=("times new roman", 10), bg='white').pack(anchor=W, pady=5)
        self.entry_name = Entry(fields_frame, font=("times new roman", 10), width=30)
        self.entry_name.pack(anchor=W, pady=5)
        
        # Quantity
        Label(fields_frame, text="Quantity:", font=("times new roman", 10), bg='white').pack(anchor=W, pady=5)
        self.entry_qty = Entry(fields_frame, font=("times new roman", 10), width=30)
        self.entry_qty.pack(anchor=W, pady=5)
        
        # Price
        Label(fields_frame, text="Unit Price:", font=("times new roman", 10), bg='white').pack(anchor=W, pady=5)
        self.entry_price = Entry(fields_frame, font=("times new roman", 10), width=30)
        self.entry_price.pack(anchor=W, pady=5)
        
        # Receipt type
        Label(fields_frame, text="Receipt Type:", font=("times new roman", 10), bg='white').pack(anchor=W, pady=5)
        self.receipt_type_var = StringVar(value="purchase")
        type_frame = Frame(fields_frame, bg='white')
        type_frame.pack(anchor=W, pady=5)
        Radiobutton(type_frame, text="Purchase", variable=self.receipt_type_var, value="purchase", bg='white').pack(side=LEFT, padx=5)
        Radiobutton(type_frame, text="Sales", variable=self.receipt_type_var, value="sales", bg='white').pack(side=LEFT, padx=5)
        
        # Add button
        add_btn = Button(
            fields_frame,
            text="➕ Add Item",
            command=self.add_manual_item,
            font=("times new roman", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            padx=20,
            pady=8
        )
        add_btn.pack(pady=20)
        
        # Right panel - Items list
        right_panel = Frame(parent, bg='white')
        right_panel.pack(side=RIGHT, fill=BOTH, padx=10, pady=10, expand=True)
        
        items_label = Label(
            right_panel,
            text="Items in Receipt",
            font=("times new roman", 14, "bold"),
            bg='white'
        )
        items_label.pack(pady=10)
        
        # Items table
        table_frame = Frame(right_panel, bg='white', relief=RIDGE, bd=2)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        columns = ('Product', 'Qty', 'Price', 'Total')
        self.items_tree = ttk.Treeview(table_frame, columns=columns, height=10, show='headings', yscrollcommand=scrollbar.set)
        
        # Define column headings
        widths = [150, 60, 80, 80]
        for i, col in enumerate(columns):
            self.items_tree.column(col, width=widths[i])
            self.items_tree.heading(col, text=col)
        
        self.items_tree.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.items_tree.yview)
        
        # Delete button
        delete_btn = Button(
            right_panel,
            text="🗑️ Delete Selected",
            command=self.delete_manual_item,
            font=("times new roman", 10, "bold"),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        delete_btn.pack(pady=10)
        
        # Process button
        process_manual_btn = Button(
            right_panel,
            text="✔️ Process Receipt",
            command=self.process_manual_receipt,
            font=("times new roman", 11, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            padx=20,
            pady=10
        )
        process_manual_btn.pack(pady=10)
    
    def create_history_tab(self, parent):
        """Create history tab"""
        history_label = Label(
            parent,
            text="Recent Receipt History",
            font=("times new roman", 14, "bold"),
            bg='white'
        )
        history_label.pack(pady=10)
        
        # History table
        table_frame = Frame(parent, bg='white')
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview for history
        columns = ('Receipt ID', 'Type', 'Date', 'Items', 'Amount', 'Status')
        self.history_tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        # Define column headings and widths
        widths = [100, 80, 150, 60, 100, 100]
        for i, col in enumerate(columns):
            self.history_tree.column(col, width=widths[i])
            self.history_tree.heading(col, text=col)
        
        self.history_tree.pack(fill=BOTH, expand=True)
        
        # Refresh button
        refresh_btn = Button(
            parent,
            text="🔄 Refresh",
            command=self.load_receipt_history,
            font=("times new roman", 10, "bold"),
            bg="#009688",
            fg="white",
            cursor="hand2",
            padx=20,
            pady=8
        )
        refresh_btn.pack(pady=10)
        
        # Load initial history
        self.load_receipt_history()
    
    def select_file(self):
        """Open file dialog to select receipt"""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Receipt File",
            filetypes=file_types
        )
        
        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.file_label.config(text=f"✓ Selected: {file_name}", fg='green')
    
    def add_manual_item(self):
        """Add item to manual list"""
        name = self.entry_name.get().strip()
        qty_str = self.entry_qty.get().strip()
        price_str = self.entry_price.get().strip()
        
        if not name or not qty_str or not price_str:
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        try:
            qty = int(qty_str)
            price = float(price_str)
            
            if qty <= 0 or price <= 0:
                messagebox.showwarning("Warning", "Quantity and price must be greater than 0")
                return
            
            # Add to list
            self.manual_items.append({
                'name': name,
                'qty': qty,
                'price': price
            })
            
            # Update tree
            total = qty * price
            self.items_tree.insert('', 'end', values=(name, qty, f"₹{price:.2f}", f"₹{total:.2f}"))
            
            # Clear entries
            self.entry_name.delete(0, END)
            self.entry_qty.delete(0, END)
            self.entry_price.delete(0, END)
            self.entry_name.focus()
            
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number and price must be a valid decimal")
    
    def delete_manual_item(self):
        """Delete selected item from manual list"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        # Get index
        item = selection[0]
        index = self.items_tree.index(item)
        
        # Remove from list and tree
        self.manual_items.pop(index)
        self.items_tree.delete(item)
    
    def process_manual_receipt(self):
        """Process manually entered receipt"""
        if not self.manual_items:
            messagebox.showwarning("Warning", "Please add items first")
            return
        
        # Create temporary file name
        temp_file = "manual_receipt.jpg"
        
        # Set receipt type
        receipt_type = self.receipt_type_var.get()
        
        # Process using handler with manual items
        result = self.handler.process_receipt_workflow(
            temp_file,
            manual_items=self.manual_items,
            receipt_type_override=receipt_type
        )
        
        if result['success']:
            messagebox.showinfo(
                "Success",
                f"Receipt processed successfully!\n\n"
                f"Receipt ID: {result['receipt_id']}\n"
                f"Items Processed: {len(result['processed_items'])}\n"
                f"Message: {result['message']}"
            )
            self.load_receipt_history()
            self.manual_items.clear()
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)
        else:
            # Show detailed error
            error_msg = f"Failed to process receipt:\n{result['message']}\n\n"
            if result['failed_items']:
                error_msg += "Failed Items:\n"
                for item in result['failed_items']:
                    error_msg += f"- {item['name']}: {item['reason']}\n"
            messagebox.showerror("Error", error_msg)
    
    def process_receipt(self):
        """Process the selected receipt"""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a receipt file first")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, END)
        self.results_text.insert(END, "Processing receipt...\n")
        self.root.update()
        
        # Process receipt
        result = self.handler.process_receipt_workflow(self.selected_file)
        
        # Display results
        self.display_results(result)
        
        # Reload history
        self.load_receipt_history()
        
        # Show status message
        if result['success']:
            messagebox.showinfo(
                "Success",
                f"Receipt processed successfully!\n\n{result['message']}"
            )
        else:
            messagebox.showerror(
                "Error",
                f"Failed to process receipt:\n{result['message']}"
            )
    
    def display_results(self, result):
        """Display processing results in the results text area"""
        self.results_text.delete(1.0, END)
        
        # Header
        self.results_text.insert(END, "=" * 50 + "\n")
        self.results_text.insert(END, "RECEIPT PROCESSING RESULTS\n")
        self.results_text.insert(END, "=" * 50 + "\n\n")
        
        # Receipt info
        self.results_text.insert(END, f"Status: {'✓ SUCCESS' if result['success'] else '✗ FAILED'}\n")
        self.results_text.insert(END, f"Receipt ID: {result['receipt_id'] or 'N/A'}\n")
        self.results_text.insert(END, f"Message: {result['message']}\n\n")
        
        # Processed items
        if result['processed_items']:
            self.results_text.insert(END, "PROCESSED ITEMS:\n")
            self.results_text.insert(END, "-" * 50 + "\n")
            for item in result['processed_items']:
                self.results_text.insert(
                    END,
                    f"• {item['name']}\n"
                    f"  Qty: {item['qty']} | "
                    f"Old: {item['old_qty']} → New: {item['new_qty']}\n"
                    f"  Action: {item['action'].upper()}\n\n"
                )
        
        # Failed items
        if result['failed_items']:
            self.results_text.insert(END, "FAILED ITEMS:\n")
            self.results_text.insert(END, "-" * 50 + "\n")
            for item in result['failed_items']:
                self.results_text.insert(
                    END,
                    f"✗ {item['name']}\n"
                    f"  Reason: {item['reason']}\n\n"
                )
        
        self.results_text.insert(END, "=" * 50 + "\n")
    
    def load_receipt_history(self):
        """Load and display recent receipt history"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Fetch recent receipts
        receipts = self.handler.get_receipt_history(limit=15)
        
        # Populate table
        for receipt in receipts:
            # receipt format: (receipt_id, receipt_type, upload_date, file_name, total_items, total_amount, status, notes)
            self.history_tree.insert(
                '',
                'end',
                values=(
                    receipt[0],  # Receipt ID
                    receipt[1].upper(),  # Type
                    receipt[2],  # Date
                    receipt[4],  # Items
                    f"₹{receipt[5]:.2f}",  # Amount
                    receipt[6]  # Status
                )
            )


def open_receipt_window(parent_root):
    """Open Receipt Processing window"""
    receipt_window = Toplevel(parent_root)
    receipt_window.geometry("1400x900")
    ui = ReceiptProcessingUI(receipt_window)
    return receipt_window

