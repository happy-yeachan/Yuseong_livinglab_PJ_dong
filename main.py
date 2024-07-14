import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QGridLayout
)

from honor_of_war.honor_of_war_main import HonorScreen
from veterans_honor.veterans_honor_main import VeteranScreen
from veterans_spouse.veterans_spouse_main import SpouseScreen

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # 버튼 3개 추가 및 크기 조정
        self.honor_button = QPushButton('참전 명예')
        self.honor_button.setFixedSize(250, 150)  # 고정 크기 설정
        self.honor_button.clicked.connect(lambda: self.set_screen(1))
        layout.addWidget(self.honor_button, 0, 0)

        self.veteran_button = QPushButton('보훈 예우')
        self.veteran_button.setFixedSize(250, 150)  # 고정 크기 설정
        self.veteran_button.clicked.connect(lambda: self.set_screen(2))
        layout.addWidget(self.veteran_button, 0, 1)

        self.spouse_button = QPushButton('보훈 예우 배우자')
        self.spouse_button.setFixedSize(250, 150)  # 고정 크기 설정
        self.spouse_button.clicked.connect(lambda: self.set_screen(3))
        layout.addWidget(self.spouse_button, 0, 2)

        # 레이아웃 설정
        self.setLayout(layout)
        
        # 윈도우 타이틀 설정
        self.setWindowTitle('메인 화면')

    def set_screen(self, idx):
        self.parentWidget().setCurrentIndex(idx)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    main_window = MainWindow()
    honor_screen = HonorScreen()
    veteran_screen = VeteranScreen()
    spouse_screen = SpouseScreen()

    stacked_widget.addWidget(main_window)
    stacked_widget.addWidget(honor_screen)
    stacked_widget.addWidget(veteran_screen)
    stacked_widget.addWidget(spouse_screen)

    # 스택드 위젯을 최대화 모드로 표시
    stacked_widget.showMaximized()

    sys.exit(app.exec_())
