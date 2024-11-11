from data_control import *
from PyQt5.QtWidgets import QMessageBox
import datetime
from openpyxl import Workbook


def show_new(screen):
    screen.reset_button_styles()
    screen.new_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급 신규자')
    configure_new_table(screen)
    rows = get_data("Honor_of_War_New")
    screen.load_data(rows, 'new')

def configure_new_table(screen):
    screen.table.setColumnCount(13)
    screen.table.setHorizontalHeaderLabels([
        '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '입금유형', '은행명', '예금주', '계좌번호', '신규 사유', '전입일', '비고'
    ])

def new_submit_form(screen):
    if new_validate_form(screen):
        tmp = add_new_Honor_of_War(new_get_form_data(screen))
        if tmp:
            show_message("이미 등록된 보훈번호입니다.")
        else:
            rows = get_data("Honor_of_War_New")
            screen.load_data(rows, 'new')
            show_message("데이터가 성공적으로 추가되었습니다.")

def new_get_form_data(screen):
    return (
        screen.dong_name.currentText(),
        datetime.datetime.now().strftime("%Y.%m.%d"),  # 현재 날짜
        screen.honor_number.text(),
        screen.name.text(),
        screen.resident_number.text(),
        f"{screen.address.text()}({screen.detail_address.text()})",
        screen.deposit_type.currentText(),
        screen.bank_name.currentText(),
        screen.depositor_name.text(),
        screen.account_number.text(),
        screen.new_reason.text(),
        screen.transfer_date.text(),
        screen.notes.toPlainText()
    )

def new_validate_form(screen):
    # 필수 입력 필드가 비어 있는지 확인
    required_fields = {
        '동명': screen.dong_name.currentText(),
        '보훈번호': screen.honor_number.text(),
        '성명': screen.name.text(),
        '주민번호': screen.resident_number.text(),
        '기본 주소': screen.address.text(),
        '상세 주소': screen.detail_address.text(),
        '입금유형': screen.deposit_type.currentText(),
        '은행명': screen.bank_name.currentText(),
        '예금주': screen.depositor_name.text(),
        '계좌번호': screen.account_number.text(),
        '신규 사유': screen.new_reason.text(),
        '전입일': screen.transfer_date.text()
    }

    for field, value in required_fields.items():
        if not value:
            show_message(f"{field} 필드를 입력해주세요.")
            return False

    # 각 필드의 형식이 올바른지 확인
    
    rrn = screen.resident_number.text().replace("-", "")
    if not rrn.isdigit() or len(rrn) != 13:
        show_message("주민번호는 13자리 숫자여야 합니다.")
        screen.resident_number.setFocus()
        return False

    if len(screen.account_number.text()) < 10:
        show_message("계좌번호는 최소 10자리 이상이어야 합니다.")
        screen.account_number.setFocus()
        return False


    # 모든 유효성 검사를 통과하면 True 반환
    return True

def show_message(message):
    QMessageBox.information(None, '정보', message)

def new_load_selected_data(screen, row, column):
    screen.selected_row = row
    set_form_fields_from_table(screen, row)
    configure_buttons_for_edit(screen)

    set_focus_for_column(screen, column)

def set_form_fields_from_table(screen, row):
    screen.dong_name.setCurrentText(screen.table.item(row, 0).text())
    screen.honor_number.setText(screen.table.item(row, 2).text())
    screen.honor_number.setReadOnly(True)
    screen.name.setText(screen.table.item(row, 3).text())
    screen.resident_number.setText(screen.table.item(row, 4).text())
    address_parts = screen.table.item(row, 5).text().split('(')
    screen.address.setText(address_parts[0][:-1])
    screen.detail_address.setText(address_parts[1][:-1])
    screen.deposit_type.setCurrentText(screen.table.item(row, 6).text())
    screen.bank_name.setCurrentText(screen.table.item(row, 7).text())
    screen.depositor_name.setText(screen.table.item(row, 8).text())
    screen.account_number.setText(screen.table.item(row, 9).text())
    screen.new_reason.setText(screen.table.item(row, 10).text())
    screen.transfer_date.setText(screen.table.item(row, 11).text())
    if screen.table.item(row, 12):
        screen.notes.setPlainText(screen.table.item(row, 12).text())

def configure_buttons_for_edit(screen):
    screen.new_submit_button.setVisible(False)
    screen.new_edit_button.setVisible(True)
    screen.new_delete_button.setVisible(True)
    screen.new_cancel_button.setVisible(True)

def set_focus_for_column(screen, column):
    focus_map = {
        0: screen.dong_name,
        3: screen.name,
        4: screen.resident_number,
        5: screen.address,
        6: screen.deposit_type,
        7: screen.bank_name,
        8: screen.depositor_name,
        9: screen.account_number,
        10: screen.new_reason,
        11: screen.transfer_date,
        12: screen.notes
    }
    if column in focus_map:
        focus_map[column].setFocus()

def new_cancel(screen):
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
        screen.honor_number.setReadOnly(False)
        show_new(screen)

def new_delete(screen):
    # 사용자에게 제거할 것인지 확인하는 메시지 박스 생성
    reply = QMessageBox.question(
        screen, 
        '제거 취소', 
        '정말로 제거하시겠습니까?', 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.Yes
    )
    if reply == QMessageBox.Yes:
        delete_new_Honor_of_War(screen.honor_number.text())
        screen.honor_number.setReadOnly(False)
        rows = get_data("Honor_of_War_New")
        screen.load_data(rows, 'new')
        show_message("데이터가 성공적으로 삭제되었습니다.")
        
def new_update(screen):
    # 사용자에게 수정할 것인지 확인하는 메시지 박스 생성
    reply = QMessageBox.question(
        screen, 
        '수정 취소', 
        '정말로 수정하시겠습니까?', 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.Yes
    )
    if reply == QMessageBox.Yes:
        if new_validate_form(screen):
            update_new_Honor_of_War(screen.honor_number.text(), new_get_form_data(screen))
            rows = get_data("Honor_of_War_New")
            screen.load_data(rows, 'new')
            screen.honor_number.setEditable(True)
            show_message("데이터가 성공적으로 수정되었습니다.")
