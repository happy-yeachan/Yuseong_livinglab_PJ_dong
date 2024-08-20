from data_control import *
from openpyxl import Workbook
import datetime
from PyQt5.QtWidgets import QMessageBox

def show_current(screen):
    screen.reset_button_styles()
    screen.current_button.setStyleSheet('background-color: lightblue')
    screen.label.setText('참전 명예 수당 지급자 현황')
    screen.table.setColumnCount(13)
    screen.table.setHorizontalHeaderLabels([
        '동', '입력날짜', '보훈번호', '성명', '주민번호', '주소',
        '입금유형', '은행명', '예금주', '계좌번호', '신규 사유', '전입일', '비고'
    ])
    rows = get_data("Honor_of_War_Current")

    screen.load_data(rows, 'now')

def export_to_excel_Now():
    wb = Workbook()
    ws = wb.active
    ws.title = "참전유공자_현황"

    # 헤더 추가
    headers = [
        '동', '등록일', '보훈번호', '성명', '주민번호',
        '주소', '입금유형', '은행명', '예금주', '계좌번호',
        '신규사유', '전입일', '비고'
    ]
    ws.append(headers)

    rows = get_data("Honor_of_War_Current")

    # 데이터 추가
    for row in rows:
        ws.append(row)
        
    # 모든 열의 크기 자동 조정
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except TypeError:
                pass
        # 열 너비 설정
        adjusted_width = (max_length + 3)
        ws.column_dimensions[column_letter].width = adjusted_width

    # 파일 이름 생성 (현재 날짜 기반)
    current_date = datetime.datetime.now().strftime("%Y%m")
    file_name = f"참전유공자_현황_{current_date}.xlsx"

    # 엑셀 파일 저장
    wb.save(file_name)
    QMessageBox.information(None, "엑셀추출", f"파일명: {file_name} \n성공적으로 저장되었습니다!")