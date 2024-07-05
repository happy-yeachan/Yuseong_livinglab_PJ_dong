from data_control import *


def show_current(screen, table_name):
    screen.reset_button_styles()
    screen.current_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급자 현황')
    screen.table.setColumnCount(14)
    screen.table.setHorizontalHeaderLabels([
        'Index', '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '입금유형', '은행명', '예금주', '계좌번호', '신규 사유', '전입일', '비고'
    ])
    rows = get_data(table_name)

    # 폼 필드 전환
    screen.switch_form_fields('current')
    
    screen.table.setRowCount(len(rows))

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            screen.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))