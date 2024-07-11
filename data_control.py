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
    `Reason_date` TEXT,
    `Note` TEXT,
    `Deposit_Type` TEXT NOT NULL,
    `Bank` TEXT NOT NULL,
    `Depositor` TEXT NOT NULL,
    `Account` TEXT NOT NULL
)
''')


def get_data(table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows

def add_new_veterans(table_name, db):
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

def delete_new_veterans(table_name, honor_number):
    try:
        cursor.execute(f'DELETE FROM {table_name}_New WHERE Veteran = ?', (honor_number,))
        cursor.execute(f'DELETE FROM {table_name}_Current WHERE Veteran = ?', (honor_number,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_new_veterans(table_name, honor_number, db):
    try:
        cursor.execute(f'''
            UPDATE {table_name}_New
            SET Dong = ?, Registration_month = ?, Veteran = ?, Name = ?, RRN = ?, Address = ?, Deposit_Type = ?, Bank = ?, Depositor = ?, Account = ?, Reason = ?, Move_in = ?, Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_number))
        
        cursor.execute(f'''
            UPDATE {table_name}_Current
            SET Dong = ?, Registration_month = ?, Veteran = ?, Name = ?, RRN = ?, Address = ?, Deposit_Type = ?, Bank = ?, Depositor = ?, Account = ?, Reason = ?, Move_in = ?, Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_number))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def add_stop_veterans(table_name, db, honor_number):
    try:
        # 보훈번호로 현재 테이블에서 데이터 조회
        cursor.execute(f'SELECT Deposit_Type, Bank, Depositor, Account, Note FROM {table_name}_Current WHERE Veteran = ?', (honor_number,))
        rows = cursor.fetchall()
        
        if rows:
            # 중지 테이블에 데이터 삽입
            cursor.execute(f'''
                INSERT INTO {table_name}_Stop (Dong, Registration_month, Veteran, Name, RRN, Address, Move_in, Reason, Reason_date, Note, Deposit_Type, Bank, Depositor, Account)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', db + rows[0][:4])
            
            # 현재 테이블에서 해당 데이터 삭제
            cursor.execute(f'DELETE FROM {table_name}_Current WHERE Veteran = ?', (honor_number,))
            
            # 신규 테이블 업데이트
            cursor.execute(f'''
                UPDATE {table_name}_New
                SET Note = ?
                WHERE Veteran = ?
            ''', (rows[0][3] + " 중지됨", honor_number))
            
            conn.commit()
        else:
            print(f"Error: Veteran with honor number {honor_number} not found in Current table")
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def get_veteran_by_honor_number(honor_number):
    cursor.execute('SELECT * FROM Veterans_Current WHERE Veteran = ?', (honor_number,))
    return cursor.fetchone()