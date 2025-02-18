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
        '전입일', '중단사유', '년월일', '비고'
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
        screen.address.text(),
        screen.transfer_date.text(),
        screen.stop_reason.text(),
        screen.stop_date.text(),
        screen.notes.toPlainText()
    )

def stop_get_form_data_for_update(screen):
    return (
        screen.stop_reason.text(),
        screen.stop_date.text(),
        screen.notes.toPlainText()
    )

def stop_validate_form(screen):
    # 필수 입력 필드가 비어 있는지 확인
    required_fields = {
        '중단사유': screen.stop_reason.text(),
        '년월일': screen.stop_date.text()
    }

    for field, value in required_fields.items():
        if not value:
            show_message(f"{field} 필드를 입력해주세요.")
            return False

    # 각 필드의 형식이 올바른지 확인
    
    date = screen.stop_date.text().replace(".", "")
    if not date.isdigit() or len(date) != 8:
        show_message("날짜는 0000.00.00 형식의 숫자여야 합니다.")
        screen.stop_date.setFocus()
        return False
    
    # 모든 유효성 검사를 통과하면 True 반환
    return True

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
    screen.address.setText(screen.table.item(row, 5).text())
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
    if reply == QMessageBox.Yes and stop_validate_form(screen):
        update_stop_Honor_of_War(screen.honor_number.text(), stop_get_form_data_for_update(screen))
        rows = get_data("Honor_of_War_stop")
        screen.load_data(rows, 'stop')
        show_message("데이터가 성공적으로 수정되었습니다.")


def search_veteran(screen, honor_number):
    if honor_number:
        row = get_Honor_of_War_by_honor_number(str(honor_number))
        if row:
            screen.dong_name.setText(row[0])
            screen.name.setText(row[3])
            screen.resident_number.setText(row[4])
            screen.address.setText(row[5])
            screen.transfer_date.setText(row[11])
        else:
            QMessageBox.information(screen, '검색 결과 없음', '해당 보훈번호로 등록된 사용자를 찾을 수 없습니다.')
