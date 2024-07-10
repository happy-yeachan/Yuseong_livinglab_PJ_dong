from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3


conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS Veterans_Current (
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL PRIMARY KEY,
    `Name` TEXT NOT NULL,
    `RRN` TEXT NOT NULL,
    `Address` TEXT NOT NULL,
    `Deposit_Type` TEXT NOT NULL,
    `Bank` TEXT NOT NULL,
    `Depositor` TEXT NOT NULL,
    `Account` TEXT NOT NULL,
    `Reason` TEXT NOT NULL,
    `Move_in` TEXT NOT NULL,
    `Note` TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Veterans_New (
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL PRIMARY KEY,
    `Name` TEXT NOT NULL,
    `RRN` TEXT NOT NULL,
    `Address` TEXT NOT NULL,
    `Deposit_Type` TEXT NOT NULL,
    `Bank` TEXT NOT NULL,
    `Depositor` TEXT NOT NULL,
    `Account` TEXT NOT NULL,
    `Reason` TEXT NOT NULL,
    `Move_in` TEXT NOT NULL,
    `Note` TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Veterans_Stop (
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL PRIMARY KEY,
    `Name` TEXT NOT NULL,
    `RRN` TEXT NOT NULL,
    `Address` TEXT NOT NULL,
    `Move_in` TEXT,
    `Reason` TEXT NOT NULL,
    `Reason_data` TEXT,
    `Note` TEXT
)
''')



def get_data(table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows

def add_data_veterans(table_name, db):
    try:
        cursor.execute(f'''
            INSERT INTO {table_name}_New (Dong, Registration_month, Veteran, Name, RRN, Address, Deposit_Type, Bank, Depositor, Account, Reason, Move_in, Note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', db)
        cursor.execute(f'''
            INSERT INTO {table_name}_Current (Dong, Registration_month, Veteran, Name, RRN, Address, Deposit_Type, Bank, Depositor, Account, Reason, Move_in, Note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', db)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Duplicate Veteran entry")

def delete_data_veterans(table_name, honor_number):
    try:
        cursor.execute(f'DELETE FROM {table_name}_New WHERE Veteran = ?', (honor_number,))
        cursor.execute(f'DELETE FROM {table_name}_Current WHERE Veteran = ?', (honor_number,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_data_veterans(table_name, honor_name, db):
    try:
        cursor.execute(f'''
            UPDATE {table_name}_New
            SET Dong = ?, Registration_month = ?, Veteran = ?, Name = ?, RRN = ?, Address = ?, Deposit_Type = ?, Bank = ?, Depositor = ?, Account = ?, Reason = ?, Move_in = ?, Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_name))
        
        cursor.execute(f'''
            UPDATE {table_name}_Current
            SET Dong = ?, Registration_month = ?, Veteran = ?, Name = ?, RRN = ?, Address = ?, Deposit_Type = ?, Bank = ?, Depositor = ?, Account = ?, Reason = ?, Move_in = ?, Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_name))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
