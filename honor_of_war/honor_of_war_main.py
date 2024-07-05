from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
import sqlite3

conn = sqlite3.connect('honor_of_war/honor_of_war_databases/honor_of_war_current.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Veterans (
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

class HonorScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.current_button = None

        layout = QVBoxLayout()

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        back_button = QPushButton('이전')
        back_button.clicked.connect(self.go_back)

        self.current_button = QPushButton('현황')
        self.current_button.clicked.connect(self.show_current)

        self.new_button = QPushButton('신규자')
        self.new_button.clicked.connect(self.show_new)

        self.stop_button = QPushButton('중지자')
        self.stop_button.clicked.connect(self.show_stopped)

        button_layout.addWidget(back_button)
        button_layout.addWidget(self.current_button)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.stop_button)

        self.label = QLabel()
        self.table = QTableWidget()

        self.show_current()

        layout.addLayout(button_layout)
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.show_current()

    def go_back(self):
        self.parentWidget().setCurrentIndex(0)

    def show_current(self):
        self.reset_button_styles()
        self.current_button.setStyleSheet('background-color: lightblue')
        self.label.setText('참전 명예 수당 지급자 현황')
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels([
            'Index', 'Dong', 'Registration_month', 'Veteran', 'Name', 'RRN', 'Address',
            'Deposit_Type', 'Bank', 'Depositor', 'Account', 'Reason', 'Move_in', 'Note'
        ])
        self.load_data()

    def show_new(self):
        self.reset_button_styles()
        self.new_button.setStyleSheet('background-color: lightblue')
        self.label.setText('참전 명예 수당 지급 신규자')
        # 데이터 로드 함수 호출 필요 시 추가

    def show_stopped(self):
        self.reset_button_styles()
        self.stop_button.setStyleSheet('background-color: lightblue')
        self.label.setText('참전 명예 수당 지급 중지자')
        # 데이터 로드 함수 호출 필요 시 추가

    def reset_button_styles(self):
        self.current_button.setStyleSheet('')
        self.new_button.setStyleSheet('')
        self.stop_button.setStyleSheet('')

    def load_data(self):
        cursor.execute('SELECT * FROM Veterans')
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
