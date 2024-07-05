import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout
)

from honor_of_war.honor_of_war_main import *
from veterans_honor.veterans_honor_main import *
from veterans_spouse.veterans_spouse_main import *
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 버튼 3개 추가
        self.honor_button = QPushButton('참전 명예')
        self.honor_button.clicked.connect(self.set_screen(1))
        layout.addWidget(self.honor_button)

        self.veteran_button = QPushButton('보훈 예우')
        self.veteran_button.clicked.connect(self.set_screen(2))
        layout.addWidget(self.veteran_button)

        self.spouse_button = QPushButton('보훈 예우 배우자')
        self.spouse_button.clicked.connect(self.set_screen(3))
        layout.addWidget(self.spouse_button)

        self.setLayout(layout)
        self.setWindowTitle('메인 화면')
        self.setGeometry(100, 100, 300, 200)

    def set_screen(self, idx):
        self.parent().setCurrentIndex(idx)

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

    stacked_widget.setFixedWidth(400)
    stacked_widget.setFixedHeight(300)
    stacked_widget.show()

    sys.exit(app.exec_())
