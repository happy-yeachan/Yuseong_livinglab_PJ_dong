from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem
)

from honor_of_war.honor_of_war_current import *
from honor_of_war.honor_of_war_new import *
from honor_of_war.honore_of_war_stop import *

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
        self.new_button.clicked.connect(lambda: show_new(self, 'Veterans_New'))

        self.stop_button = QPushButton('중지자')
        self.stop_button.clicked.connect(lambda: show_stop(self, 'Veterans_Stop'))

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

    def reset_button_styles(self):
        self.current_button.setStyleSheet('')
        self.new_button.setStyleSheet('')
        self.stop_button.setStyleSheet('')