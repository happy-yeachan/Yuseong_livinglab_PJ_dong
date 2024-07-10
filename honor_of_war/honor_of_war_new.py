from data_control import *
from PyQt5.QtWidgets import QMessageBox
import datetime

def show_new(screen):
    screen.reset_button_styles()
    screen.new_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급 신규자')
    configure_new_table(screen)
    rows = get_data("Veterans_New")
    screen.load_data(rows, 'new')

def configure_new_table(screen):
    screen.table.setColumnCount(14)
    screen.table.setHorizontalHeaderLabels([
        'Index', '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '입금유형', '은행명', '예금주', '계좌번호', '신규 사유', '전입일', '비고'
    ])

def submit_form(screen):
    if validate_form(screen):
        add_data_veterans('Veterans', get_form_data(screen))
        rows = get_data("Veterans_New")
        screen.load_data(rows, 'new')
        show_message("데이터가 성공적으로 추가되었습니다.")
    else:
        show_message("모든 필드를 정확히 입력하세요.")

def get_form_data(screen):
    return (
        screen.dong_name.text(),
        datetime.datetime.now().strftime("%Y.%m.%d"),  # 현재 날짜
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
    )

def validate_form(screen):
    # 예시: 빈 필드가 있는지 확인하는 간단한 검증 로직
    return all([
        screen.dong_name.text(),
        screen.honor_number.text(),
        screen.name.text(),
        screen.resident_number.text(),
        screen.zip_code.text(),
        screen.address.text(),
        screen.detail_address.text(),
        screen.deposit_type.currentText(),
        screen.bank_name.currentText(),
        screen.depositor_name.text(),
        screen.account_number.text(),
        screen.new_reason.text(),
        screen.transfer_date.text()
    ])

def show_message(message):
    QMessageBox.information(None, '정보', message)

def load_selected_data(screen, row, column):
    screen.selected_row = row
    set_form_fields_from_table(screen, row)
    configure_buttons_for_edit(screen)

    set_focus_for_column(screen, column)

def set_form_fields_from_table(screen, row):
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

def configure_buttons_for_edit(screen):
    screen.submit_button.setVisible(False)
    screen.edit_button.setVisible(True)
    screen.delete_button.setVisible(True)
    screen.cancel_button.setVisible(True)

def set_focus_for_column(screen, column):
    focus_map = {
        1: screen.dong_name,
        3: screen.honor_number,
        4: screen.name,
        5: screen.resident_number,
        6: screen.zip_code,
        7: screen.deposit_type,
        8: screen.bank_name,
        9: screen.depositor_name,
        10: screen.account_number,
        11: screen.new_reason,
        12: screen.transfer_date,
        13: screen.notes,
    }
    if column in focus_map:
        focus_map[column].setFocus()


def edit_cancel(screen):
    # 사용자에게 취소할 것인지 확인하는 메시지 박스 생성
    reply = QMessageBox.question(
        screen, 
        '취소 확인', 
        '정말로 취소하시겠습니까?', 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.Yes
    )
    
    # 사용자가 'Yes'를 클릭한 경우에만 'show_new' 함수 호출
    if reply == QMessageBox.Yes:
        show_new(screen)
