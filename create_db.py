import sqlite3

def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS receipt_logs(receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,receipt_type text,upload_date text,file_name text,total_items INTEGER,total_amount REAL,status text,notes text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS receipt_items(item_id INTEGER PRIMARY KEY AUTOINCREMENT,receipt_id INTEGER,product_id INTEGER,product_name text,quantity INTEGER,unit_price REAL,total_price REAL,action text,FOREIGN KEY(receipt_id) REFERENCES receipt_logs(receipt_id),FOREIGN KEY(product_id) REFERENCES product(pid))")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS transaction_logs(txn_id INTEGER PRIMARY KEY AUTOINCREMENT,receipt_id INTEGER,product_id INTEGER,product_name text,quantity INTEGER,action text,old_qty INTEGER,new_qty INTEGER,timestamp text,FOREIGN KEY(receipt_id) REFERENCES receipt_logs(receipt_id),FOREIGN KEY(product_id) REFERENCES product(pid))")
    con.commit()


create_db()