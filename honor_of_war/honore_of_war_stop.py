from data_control import *
from PyQt5.QtWidgets import QTableWidget

def show_stop(screen, table_name):
    screen.reset_button_styles()
    screen.stop_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급 중지자')
    screen.table.setColumnCount(11)
    screen.table.setHorizontalHeaderLabels([
        'Index', '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '전입일', '중단사유', '사유일시', '비고'
    ])
    rows = get_data(table_name)

    screen.table.setRowCount(len(rows))

    # 폼 필드 전환
    screen.switch_form_fields('stop')

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            screen.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    screen.table.resizeColumnsToContents()  # 자동으로 모든 열의 너비를 조정하여 내용을 맞춤
    screen.table.setMinimumWidth(1000) 
    screen.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)