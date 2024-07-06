from data_control import *
from PyQt5.QtWidgets import QTableWidget

def show_stop(screen):
    screen.reset_button_styles()
    screen.stop_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급 중지자')
    screen.table.setColumnCount(11)
    screen.table.setHorizontalHeaderLabels([
        'Index', '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '전입일', '중단사유', '사유일시', '비고'
    ])
    rows = get_data("Veterans_Stop")

    screen.table.setRowCount(len(rows))

    screen.load_data(rows, 'stop')