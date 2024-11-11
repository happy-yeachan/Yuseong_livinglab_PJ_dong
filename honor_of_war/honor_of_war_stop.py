from data_control import *
from PyQt5.QtWidgets import QMessageBox
import datetime
from openpyxl import Workbook

def show_stop(screen):
    screen.reset_button_styles()
    screen.stop_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급 중지자')
    configure_stop_table(screen)
    rows = get_data("Honor_of_War_Stop")
    screen.load_data(rows, 'stop')

def configure_stop_table(screen):
    screen.table.setColumnCount(10)
    screen.table.setHorizontalHeaderLabels([
        '동', '등록일', '보훈번호', '성명', '주민번호', '주소',
        '전입일', '중단사유', '사유일시', '비고'
    ])

def stop_submit_form(screen):
    if stop_validate_form(screen):
        add_stop_Honor_of_War(stop_get_form_data(screen), screen.honor_number.text())
        rows = get_data("Honor_of_War_Stop")
        screen.load_data(rows, 'stop')
        show_message("데이터가 성공적으로 추가되었습니다.")
    else:
        show_message("모든 필드를 정확히 입력하세요.")

def stop_get_form_data(screen):
    return (
        screen.dong_name.text(),
        datetime.datetime.now().strftime("%Y.%m.%d"),  # 현재 날짜
        screen.honor_number.text(),
        screen.name.text(),
        screen.resident_number.text(),
        f"{screen.address.text()} ({screen.detail_address.text()})",
        screen.transfer_date.text(),
        screen.stop_reason.text(),
        screen.stop_date.text(),
        screen.notes.toPlainText()
    )

def stop_validate_form(screen):
    # 데이터 확인 코드 추가 예정
    return all([
        screen.dong_name.text(),
        screen.honor_number.text(),
        screen.name.text(),
        screen.resident_number.text(),
        screen.address.text(),
        screen.detail_address.text(),
        screen.transfer_date.text(),
        screen.stop_reason.text(),
        screen.stop_date.text()
    ])

def show_message(message):
    QMessageBox.information(None, '정보', message)

def stop_load_selected_data(screen, row, column):
    screen.selected_row = row
    set_form_fields_from_table(screen, row)
    configure_buttons_for_edit(screen)

    set_focus_for_column(screen, column)

def set_form_fields_from_table(screen, row):
    screen.dong_name.setText(screen.table.item(row, 0).text())
    screen.honor_number.setText(screen.table.item(row, 2).text())
    screen.name.setText(screen.table.item(row, 3).text())
    screen.resident_number.setText(screen.table.item(row, 4).text())
    address_parts = screen.table.item(row, 5).text().split('(')
    screen.address.setText(address_parts[0][:-1])
    screen.detail_address.setText(address_parts[1][:-1])
    screen.transfer_date.setText(screen.table.item(row, 6).text())
    screen.stop_reason.setText(screen.table.item(row, 7).text())
    screen.stop_date.setText(screen.table.item(row, 8).text())
    if screen.table.item(row, 9):
        screen.notes.setPlainText(screen.table.item(row, 9).text())

def configure_buttons_for_edit(screen):
    screen.stop_submit_button.setVisible(False)
    screen.stop_edit_button.setVisible(True)
    screen.stop_delete_button.setVisible(True)
    screen.stop_cancel_button.setVisible(True)

def set_focus_for_column(screen, column):
    focus_map = {
        6: screen.transfer_date,
        7: screen.stop_reason,
        8: screen.stop_date,
        9: screen.notes,
    }
    if column in focus_map:
        focus_map[column].setFocus()

def stop_cancel(screen):
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
        show_stop(screen)

def stop_delete(screen):
    # 사용자에게 제거할 것인지 확인하는 메시지 박스 생성
    reply = QMessageBox.question(
        screen, 
        '복구 확인', 
        '정말로 복구하시겠습니까?', 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.Yes
    )
    if reply == QMessageBox.Yes:
        delete_stop_Honor_of_War(screen.honor_number.text())
        rows = get_data("Honor_of_War_Stop")
        screen.load_data(rows, 'stop')
        show_message("데이터가 성공적으로 복구되었습니다.")
        
def stop_update(screen):
    # 사용자에게 수정할 것인지 확인하는 메시지 박스 생성
    reply = QMessageBox.question(
        screen, 
        '수정', 
        '정말로 수정하시겠습니까?', 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.Yes
    )
    if reply == QMessageBox.Yes:
        #update_stop_veterans(screen.honor_number.text(), get_form_data(screen))
        rows = get_data("Honor_of_War_stop")
        screen.load_data(rows, 'stop')
        show_message("데이터가 성공적으로 수정되었습니다.")


def search_veteran(screen, honor_number):
    if honor_number:
        row = get_Honor_of_War_by_honor_number(honor_number)
        if row:
            screen.dong_name.setText(row[0])
            screen.name.setText(row[3])
            screen.resident_number.setText(row[4])
            address_parts = row[5].split('(')
            screen.address.setText(address_parts[0][:-1])
            screen.detail_address.setText(address_parts[1][:-1])
            screen.transfer_date.setText(row[11])
        else:
            QMessageBox.information(screen, '검색 결과 없음', '해당 보훈번호로 등록된 사용자를 찾을 수 없습니다.')
