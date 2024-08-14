from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QSpacerItem, QSizePolicy
)

from honor_of_war.honor_of_war_current import *
from honor_of_war.honor_of_war_new import *
from honor_of_war.honor_of_war_stop import *

class HonorScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.current_button = None

        layout = QVBoxLayout()

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        back_button = QPushButton('이전')
        back_button.clicked.connect(self.go_back)

        self.new_button = QPushButton('신규자')
        self.new_button.clicked.connect(lambda: show_new(self))

        self.stop_button = QPushButton('중지자')
        self.stop_button.clicked.connect(lambda: show_stop(self))

        self.current_button = QPushButton('현황')
        self.current_button.clicked.connect(lambda: show_current(self))

        button_layout.addWidget(back_button)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.current_button)

        self.label = QLabel()
        self.table = QTableWidget()

        layout.addLayout(button_layout)
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # 폼 레이아웃 추가
        self.form_layout = QFormLayout()
        self.add_form_fields('now')

         # 테이블과 폼을 가로로 나란히 배치할 레이아웃
        content_layout = QHBoxLayout()
        content_layout.addLayout(self.form_layout)
        content_layout.addWidget(self.table)

        layout.addLayout(content_layout)

        # 초기 화면 설정
        show_current(self)

        self.setLayout(layout)

    def format_resident_number(self, text):
        # '-'가 없는 숫자 부분만 추출
        numbers = text.replace("-", "")
        if len(numbers) > 6:
            # 앞 6자리를 추출하고 '-'를 추가
            formatted = numbers[:6] + '-' + numbers[6:]
            # 커서 위치를 유지하며 텍스트를 설정
            cursor_position = self.resident_number.cursorPosition()
            self.resident_number.blockSignals(True)
            self.resident_number.setText(formatted)
            self.resident_number.setCursorPosition(cursor_position + 1)
            self.resident_number.blockSignals(False)

    def go_back(self):
        self.parentWidget().setCurrentIndex(0)

    def reset_button_styles(self):
        self.current_button.setStyleSheet('')
        self.new_button.setStyleSheet('')
        self.stop_button.setStyleSheet('')

    def switch_form_fields(self, mode):
        # 기존 폼 필드 제거
        for i in reversed(range(self.form_layout.rowCount())):
            self.form_layout.removeRow(i)
        
        if mode == 'stop':
            # 중지자 폼 필드 추가
            self.honor_number = QLineEdit()
            self.form_layout.addRow('보훈번호', self.honor_number)

            # 검색 버튼
            self.search_button = QPushButton('검색')
            self.search_button.clicked.connect(lambda: search_veteran(self, self.honor_number.text()))
            self.form_layout.addRow(self.search_button)

            self.dong_name = QLineEdit()
            self.dong_name.setReadOnly(True)
            self.form_layout.addRow('동명', self.dong_name)

            self.name = QLineEdit()
            self.name.setReadOnly(True)
            self.form_layout.addRow('성명', self.name)

            self.resident_number = QLineEdit()
            self.resident_number.setReadOnly(True)
            self.form_layout.addRow('주민번호', self.resident_number)

            # 주소
            self.zip_code = QLineEdit()
            self.zip_code.setReadOnly(True)
            self.form_layout.addRow('우편번호', self.zip_code)

            self.address = QLineEdit()
            self.address.setReadOnly(True)
            self.form_layout.addRow('기본 주소', self.address)

            self.detail_address = QLineEdit()
            self.detail_address.setReadOnly(True)
            self.form_layout.addRow('상세 주소', self.detail_address)

            self.transfer_date = QLineEdit()
            self.transfer_date.setReadOnly(True)
            self.transfer_date.setPlaceholderText('YYYYMMDD 형식으로 입력하세요 (예: 19990721)')
            self.form_layout.addRow('전입일', self.transfer_date)

            self.stop_reason = QLineEdit()
            self.form_layout.addRow('중단사유', self.stop_reason)

            self.stop_date = QLineEdit()
            self.stop_date.setPlaceholderText('YYYYMMDD 형식으로 입력하세요 (예: 19990721)')
            self.form_layout.addRow('사유일시', self.stop_date)

            self.notes = QTextEdit()
            self.notes.setPlaceholderText('자유롭게 입력하세요')
            self.notes.setFixedHeight(100)
            self.form_layout.addRow('비고', self.notes)

            # Button Layout
            self.button_layout = QHBoxLayout()

            # Submit Button
            self.stop_submit_button = QPushButton('중지')
            self.stop_submit_button.clicked.connect(lambda: stop_submit_form(self))
            self.button_layout.addWidget(self.stop_submit_button)

            # Delete Button
            self.stop_delete_button = QPushButton('복구')
            self.stop_delete_button.clicked.connect(lambda: stop_delete(self))
            self.stop_delete_button.setVisible(False)
            self.button_layout.addWidget(self.stop_delete_button)

            # Edit Button
            self.stop_edit_button = QPushButton('수정')
            self.stop_edit_button.clicked.connect(lambda: stop_update(self))
            self.stop_edit_button.setVisible(False)
            self.button_layout.addWidget(self.stop_edit_button)
            

            # Cancel Button
            self.stop_cancel_button = QPushButton('취소')
            self.stop_cancel_button.clicked.connect(lambda: stop_cancel(self))
            self.stop_cancel_button.setVisible(False)
            self.button_layout.addWidget(self.stop_cancel_button)
            
            self.form_layout.addRow(self.button_layout)

            # Spacer Item
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.form_layout.addItem(spacer)

        elif mode == "new":
            # 기존 폼 필드 복원
            self.add_form_fields(mode)

        self.export_button = QPushButton('엑셀 추출하기')
        if mode == "new":
            self.export_button.clicked.connect(lambda: export_to_excel_New())
        elif mode == "stop":
            self.export_button.clicked.connect(lambda: export_to_excel_Stop())
        else:
            self.export_button.clicked.connect(lambda: export_to_excel_Now())
        self.form_layout.addRow(self.export_button)

    def add_form_fields(self, mode):
        # 동명
        self.dong_name = QComboBox()
        self.dong_name.addItems(['진잠동', '상대동', '원신흥동', '학하동', '온천1동', '온천2동', '노은1동', '노은2동', '노은3동', '신성동', '전민동', '관평동', '구즉동'])
        self.form_layout.addRow('동명', self.dong_name)

        # 보훈번호
        self.honor_number = QLineEdit()
        self.form_layout.addRow('보훈번호', self.honor_number)

        # 성명
        self.name = QLineEdit()
        # self.name.textChanged.connect(self.update_depositor_name)
        self.form_layout.addRow('성명', self.name)

        # 주민번호
        self.resident_number = QLineEdit()
        self.resident_number.textChanged.connect(self.format_resident_number)
        self.form_layout.addRow('주민번호', self.resident_number)

        # 주소
        self.zip_code = QLineEdit()
        self.form_layout.addRow('우편번호', self.zip_code)

        self.address = QLineEdit()
        self.form_layout.addRow('기본 주소', self.address)

        self.detail_address = QLineEdit()
        self.form_layout.addRow('상세 주소', self.detail_address)

        # 입금유형
        self.deposit_type = QComboBox()
        self.deposit_type.addItems(['10:계좌이체', '20:대량이체', '30:원천징수', '40:고지서', '50:CMS', '60:수표', '99:현금'])
        self.form_layout.addRow('입금유형', self.deposit_type)

        # 은행명
        self.bank_name = QComboBox()
        self.bank_name.addItems(['KB국민은행', '신한은행', '하나은행', '우리은행', 'NH농협은행', 'IBK기업은행'])
        self.form_layout.addRow('은행명', self.bank_name)

        # 예금주
        self.depositor_name = QLineEdit()
        self.form_layout.addRow('예금주', self.depositor_name)

        # 계좌번호
        self.account_number = QLineEdit()
        self.account_number.setPlaceholderText('계좌번호를 입력하세요 (예: 12345678901234)')
        self.form_layout.addRow('계좌번호', self.account_number)

        # 신규 사유
        self.new_reason = QLineEdit('전입')
        self.form_layout.addRow('신규 사유', self.new_reason)

        # 전입일
        self.transfer_date = QLineEdit()
        self.transfer_date.setPlaceholderText('YYYYMMDD 형식으로 입력하세요 (예: 19990721)')
        # self.transfer_date.textChanged.connect(self.format_date)
        self.form_layout.addRow('전입일', self.transfer_date)

        # 비고
        self.notes = QTextEdit()
        self.notes.setPlaceholderText('자유롭게 입력하세요')
        self.notes.setFixedHeight(100)
        self.form_layout.addRow('비고', self.notes)

        # Button Layout
        self.button_layout = QHBoxLayout()


        if mode == "new":
            # Submit Button
            self.new_submit_button = QPushButton('추가')
            self.new_submit_button.clicked.connect(lambda:new_submit_form(self))
            self.button_layout.addWidget(self.new_submit_button)

            # Edit Button
            self.new_edit_button = QPushButton('수정')
            self.new_edit_button.clicked.connect(lambda: new_update(self))
            self.new_edit_button.setVisible(False)
            self.button_layout.addWidget(self.new_edit_button)
            
            # Delete Button
            self.new_delete_button = QPushButton('삭제')
            self.new_delete_button.clicked.connect(lambda:new_delete(self))
            self.new_delete_button.setVisible(False)
            self.button_layout.addWidget(self.new_delete_button)

            # cancel Button
            self.new_cancel_button = QPushButton('취소')
            self.new_cancel_button.clicked.connect(lambda:new_cancel(self))
            self.new_cancel_button.setVisible(False)
            self.button_layout.addWidget(self.new_cancel_button)
            
            self.form_layout.addRow(self.button_layout)

        # Spacer Item
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.form_layout.addItem(spacer)
    
    def load_data(self, rows, type):
        self.table.setRowCount(len(rows))
        # 폼 필드 전환
        self.switch_form_fields(f'{type}')
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        self.table.resizeColumnsToContents()  # 자동으로 모든 열의 너비를 조정하여 내용을 맞춤
        self.table.setMinimumWidth(1000) 
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents) 
        self.table.horizontalHeader().setStretchLastSection(True)
        try:
            self.table.cellClicked.disconnect()  # 기존 연결 해제
        except TypeError:
            pass  # 연결이 없으면 무시
        if type == "new":
            self.table.cellClicked.connect(lambda row, column: new_load_selected_data(self, row, column))
        elif type == "stop":
            self.table.cellClicked.connect(lambda row, column: stop_load_selected_data(self, row, column))
