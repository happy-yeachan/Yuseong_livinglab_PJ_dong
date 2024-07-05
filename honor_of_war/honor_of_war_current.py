from data_control import *


def show_current(screen, table_name):
    screen.reset_button_styles()
    screen.current_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급자 현황')
    screen.table.setColumnCount(14)
    screen.table.setHorizontalHeaderLabels([
        'Index', 'Dong', 'Registration_month', 'Veteran', 'Name', 'RRN', 'Address',
        'Deposit_Type', 'Bank', 'Depositor', 'Account', 'Reason', 'Move_in', 'Note'
    ])
    rows = load_data(table_name)

    screen.table.setRowCount(len(rows))

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            screen.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))