from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3


conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS Veterans_Current (
    `Index` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL UNIQUE,
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
    `Index` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL UNIQUE,
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
    `Index` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL UNIQUE,
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

def add_data(table_name, db):
    cursor.execute(f'''
        INSERT INTO {table_name} (Dong, Registration_month, Veteran, Name, RRN, Address, Deposit_Type, Bank, Depositor, Account, Reason, Move_in, Note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', db)
    conn.commit()