from data_control import *
from PyQt5.QtWidgets import QTableWidget, QMessageBox
import datetime

def show_new(screen):
    screen.reset_button_styles()
    screen.new_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급 신규자')
    screen.table.setColumnCount(14)
    screen.table.setHorizontalHeaderLabels([
        'Index', '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '입금유형', '은행명', '예금주', '계좌번호', '신규 사유', '전입일', '비고'
    ])
    rows = get_data("Veterans_New")
    screen.load_data(rows, 'new')

def submit_or_edit_form_new(screen):
    if screen.submit_button.text() == '추가':
        submit_form(screen)
    # else:
    #     screen.update_form()

def submit_form(screen):

    add_data('Veterans_New', (
            screen.dong_name.text(),
            datetime.datetime.now().strftime("%Y.%m.%d"),  # 현재 월을 예로 추가 (혹은 필요 시 변경 가능)
            screen.honor_number.text(),
            screen.name.text(),
            screen.resident_number.text(),
            f"{screen.zip_code.text()} {screen.address.text()} {screen.detail_address.text()}",
            screen.deposit_type.currentText(),
            screen.bank_name.currentText(),
            screen.depositor_name.text(),
            screen.account_number.text(),
            screen.new_reason.text(),
            screen.transfer_date.text(),
            screen.notes.toPlainText()
        ))
    rows = get_data("Veterans_New")
    screen.load_data(rows, 'new')