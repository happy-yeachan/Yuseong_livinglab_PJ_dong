from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)


class VeteranScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 이전 버튼 추가
        back_button_layout = QHBoxLayout()
        back_button = QPushButton('이전')
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)
        back_button_layout.addStretch()

        label = QLabel('보훈 예우 화면')

        layout.addLayout(back_button_layout)
        layout.addWidget(label)
        self.setLayout(layout)

    def go_back(self):
        self.parent().setCurrentIndex(0)