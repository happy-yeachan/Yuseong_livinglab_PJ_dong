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

    add_data_veterans('Veterans', (
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

def load_selected_data(screen, row, column):
    # 테이블에서 선택된 행의 데이터를 입력 필드에 불러오기
    screen.selected_row = row  # 선택된 행의 인덱스를 저장합니다.
    screen.dong_name.setText(screen.table.item(row, 1).text())
    screen.honor_number.setText(screen.table.item(row, 3).text())
    screen.name.setText(screen.table.item(row, 4).text())
    screen.resident_number.setText(screen.table.item(row, 5).text())
    address_parts = screen.table.item(row, 6).text().split(' ')
    screen.zip_code.setText(address_parts[0])
    screen.address.setText(' '.join(address_parts[1:-1]))
    screen.detail_address.setText(address_parts[-1])
    screen.deposit_type.setCurrentText(screen.table.item(row, 7).text())
    screen.bank_name.setCurrentText(screen.table.item(row, 8).text())
    screen.depositor_name.setText(screen.table.item(row, 9).text())
    screen.account_number.setText(screen.table.item(row, 10).text())
    screen.new_reason.setText(screen.table.item(row, 11).text())
    screen.transfer_date.setText(screen.table.item(row, 12).text())
    if screen.table.item(row, 13):
        screen.notes.setPlainText(screen.table.item(row, 13).text())

    # 버튼 텍스트를 '수정하기'로 변경합니다.
    screen.submit_button.setVisible(False)
    screen.edit_button.setVisible(True)
    screen.delete_button.setVisible(True)
    screen.cancel_button.setVisible(True)

    # 클릭한 셀에 따라 포커스를 설정합니다.
    if column == 1:
        screen.dong_name.setFocus()
    elif column == 3:
        screen.honor_number.setFocus()
    elif column == 4:
        screen.name.setFocus()
    elif column == 5:
        screen.resident_number.setFocus()
    elif column == 6:
        screen.zip_code.setFocus()
    elif column == 7:
        screen.deposit_type.setFocus()
    elif column == 8:
        screen.bank_name.setFocus()
    elif column == 9:
        screen.depositor_name.setFocus()
    elif column == 10:
        screen.account_number.setFocus()
    elif column == 11:
        screen.new_reason.setFocus()
    elif column == 12:
        screen.transfer_date.setFocus()
    elif column == 13:
        screen.notes.setFocus()
