from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3


conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS Honor_of_War_Current (
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
    `New_Reason` TEXT NOT NULL,
    `Move_in` TEXT NOT NULL,
    `Note` TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Honor_of_War_New (
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
    `New_Reason` TEXT NOT NULL,
    `Move_in` TEXT NOT NULL,
    `Note` TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Honor_of_War_Stop (
    `Dong` TEXT NOT NULL,
    `Registration_month` TEXT NOT NULL,
    `Veteran` TEXT NOT NULL PRIMARY KEY,
    `Name` TEXT NOT NULL,
    `RRN` TEXT NOT NULL,
    `Address` TEXT NOT NULL,
    `Move_in` TEXT,
    `Reason` TEXT NOT NULL,
    `Reason_date` TEXT,
    `S_Note` TEXT,
    `New_Reason` TEXT NOT NULL,
    `Deposit_Type` TEXT NOT NULL,
    `Bank` TEXT NOT NULL,
    `Depositor` TEXT NOT NULL,
    `Account` TEXT NOT NULL,
    `Note` TEXT
)
''')


def get_data(table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows

def add_new_Honor_of_War(db):
    try:
        cursor.execute(f'''
            INSERT INTO Honor_of_War_New (Dong, Registration_month, Veteran, Name, RRN, Address, Deposit_Type, Bank, Depositor, Account, New_Reason, Move_in, Note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', db)
        cursor.execute(f'''
            INSERT INTO Honor_of_War_Current (Dong, Registration_month, Veteran, Name, RRN, Address, Deposit_Type, Bank, Depositor, Account, New_Reason, Move_in, Note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', db)
        conn.commit()
    except sqlite3.IntegrityError:
        return True

def delete_new_Honor_of_War(honor_number):
    try:
        cursor.execute(f'DELETE FROM Honor_of_War_New WHERE Veteran = ?', (honor_number,))
        cursor.execute(f'DELETE FROM Honor_of_War_Current WHERE Veteran = ?', (honor_number,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_new_Honor_of_War(honor_number, db):
    try:
        cursor.execute(f'''
            UPDATE Honor_of_War_New
            SET Dong = ?, Registration_month = ?, Veteran = ?, Name = ?, RRN = ?, Address = ?, Deposit_Type = ?, Bank = ?, Depositor = ?, Account = ?, New_Reason = ?, Move_in = ?, Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_number))
        
        cursor.execute(f'''
            UPDATE Honor_of_War_Current
            SET Dong = ?, Registration_month = ?, Veteran = ?, Name = ?, RRN = ?, Address = ?, Deposit_Type = ?, Bank = ?, Depositor = ?, Account = ?, New_Reason = ?, Move_in = ?, Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_number))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def get_Honor_of_War_by_honor_number(honor_number):
    query = 'SELECT * FROM Honor_of_War_Current WHERE Veteran = ?'
    cursor.execute(query, (honor_number,))
    return cursor.fetchone()

def add_stop_Honor_of_War(db, honor_number):
    try:
        # 보훈번호로 현재 테이블에서 데이터 조회
        cursor.execute(f'SELECT New_Reason, Deposit_Type, Bank, Depositor, Account, Note FROM Honor_of_War_Current WHERE Veteran = ?', (honor_number,))
        rows = cursor.fetchall()
        if rows:
            # 중지 테이블에 데이터 삽입
            cursor.execute(f'''
                INSERT INTO Honor_of_War_Stop (Dong, Registration_month, Veteran, Name, RRN, Address, Move_in, Reason, Reason_date, S_Note, New_Reason, Deposit_Type, Bank, Depositor, Account, Note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', db + rows[0])
            
            # 현재 테이블에서 해당 데이터 삭제
            cursor.execute(f'DELETE FROM Honor_of_War_Current WHERE Veteran = ?', (honor_number,))
            
            # 신규 테이블 업데이트
            cursor.execute(f'''
                UPDATE Honor_of_War_New
                SET Note = ?
                WHERE Veteran = ?
            ''', (rows[0][5] + " 중지됨", honor_number))
            
            conn.commit()
        else:
            return 0
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def delete_stop_Honor_of_War(honor_number):
    try:
        cursor.execute(f'SELECT * FROM Honor_of_War_Stop WHERE Veteran = ?', (honor_number,))
        rows = cursor.fetchall()
        cursor.execute(f'DELETE FROM Honor_of_War_Stop WHERE Veteran = ?', (honor_number,))
        cursor.execute(f'''
            INSERT INTO Honor_of_War_Current (Dong, Registration_month, Veteran, Name, RRN, Address, Move_in, New_Reason, Deposit_Type, Bank, Depositor, Account, Note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', rows[0][0:6] + (rows[0][6],) +rows[0][10:16])

        cursor.execute(f'''
                UPDATE Honor_of_War_New
                SET Note = ?
                WHERE Veteran = ?
            ''', (rows[0][15], honor_number))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_stop_Honor_of_War(honor_number, db):
    try:
        cursor.execute(f'''
            UPDATE Honor_of_War_Stop
            SET Reason = ?, Reason_date = ?, S_Note = ?
            WHERE Veteran = ?
        ''', (*db, honor_number))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")