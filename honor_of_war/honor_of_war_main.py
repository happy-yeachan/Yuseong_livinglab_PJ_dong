from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem
)

from honor_of_war.honor_of_war_current import *

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
        self.current_button.clicked.connect(lambda: show_current(self, 'Veterans_Current'))

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

        # 초기 화면 설정
        show_current(self, 'Veterans_Current')

        layout.addLayout(button_layout)
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)


    def go_back(self):
        self.parentWidget().setCurrentIndex(0)

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

    def load_data(honor_screen, cursor, table):
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        honor_screen.table.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                honor_screen.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))