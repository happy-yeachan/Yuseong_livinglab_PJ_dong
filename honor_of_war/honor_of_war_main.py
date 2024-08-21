from PyQt5.QtWidgets import (
   QCompleter, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
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
        self.name.textChanged.connect(self.update_depositor_name)
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

        # 은행 및 증권사 리스트 (번호 포함)
        bank_list = [
            '', '001:한국은행', '002:산업은행', '003:기업은행', '004:국민은행', '005:하나은행',
            '007:수출입은행', '008:수협은행', '011:농협은행', '012:지역 농축협', '020:우리은행',
            '023:SC제일은행', '027:한국씨티은행', '031:대구은행', '032:부산은행', '034:광주은행',
            '035:제주은행', '037:전북은행', '039:경남은행', '045:새마을금고중앙회', '048:신협',
            '050:상호저축은행', '051:기타 외국계은행(중국 교통은행 등)', '052:모간스탠리은행', '054:HSBC은행',
            '055:도이치은행', '057:제이피모간체이스은행', '058:미즈호은행', '059:미쓰비시도쿄UFJ은행', 
            '060:BOA은행', '061:비엔피파리바은행', '062:중국공상은행', '063:중국은행', '064:산림조합중앙회',
            '065:대화은행', '067:중국건설은행', '071:우체국', '076:신용보증기금', '077:기술보증기금',
            '081:KEB하나은행', '088:신한은행', '089:케이뱅크', '090:카카오뱅크', '092:토스뱅크',
            '093:한국주택금융공사', '094:서울보증보험', '209:유안타증권', '218:KB증권', '221:상상인증권',
            '223:리딩투자증권', '224:BNK투자증권', '225:IBK투자증권', '226:KB증권', '227:KTB투자증권',
            '238:미래에셋대우', '240:삼성증권', '243:한국투자증권', '247:NH투자증권', '261:교보증권',
            '262:하이투자증권', '263:현대차투자증권', '264:키움증권', '265:이베스트투자증권', '266:SK증권',
            '267:대신증권', '268:메리츠종합금융증권', '269:한화투자증권', '270:하나금융투자', '271:토스증권',
            '278:신한금융투자', '279:DB금융투자', '280:유진투자증권', '287:메리츠종합금융증권', '288:카카오페이증권',
            '289:NH투자증권', '290:부국증권', '291:신영증권', '292:케이프투자증권', '294:한국포스증권'
        ]

        # 은행명 콤보박스
        self.bank_name = QComboBox()
        self.bank_name.addItems(bank_list)

        # QComboBox를 편집 가능 상태로 설정
        self.bank_name.setEditable(True)

        # QCompleter 설정
        completer = QCompleter(bank_list)
        completer.setCaseSensitivity(False)  # 대소문자 구분하지 않음
        completer.setFilterMode(Qt.MatchContains)  # 중간 단어와 일치하는 항목도 검색 가능
        self.bank_name.setCompleter(completer)

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
        self.transfer_date.setPlaceholderText('YYYYMMDD 형식으로 입력하세요')
        self.transfer_date.textChanged.connect(self.format_transfer_data)
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

    def format_transfer_data(self, text):
        # '-'가 없는 숫자 부분만 추출
        numbers = text.replace(".", "")

        # 입력된 숫자가 8자리를 초과하지 않도록 제한
        if len(numbers) > 8:
            numbers = numbers[:8]


        if len(numbers) == 8:  # 사용자가 8자리(YYYYMMDD)까지 입력했을 때
            # YYYY.MM.DD 형식으로 변환
            formatted = numbers[:4] + '.' + numbers[4:6] + '.' + numbers[6:]
            # 커서 위치를 유지하며 텍스트를 설정
            cursor_position = self.transfer_date.cursorPosition()
            self.transfer_date.blockSignals(True)
            self.transfer_date.setText(formatted)
            self.transfer_date.setCursorPosition(cursor_position + 2)  # 두 개의 '.'을 추가했으므로 커서를 2칸 앞으로 이동
            self.transfer_date.blockSignals(False)
        elif len(numbers) == 6:  # 사용자가 6자리(YYYYMM)까지 입력했을 때
            # YYYY.MM 형식으로 변환
            formatted = numbers[:4] + '.' + numbers[4:]
            cursor_position = self.transfer_date.cursorPosition()
            self.transfer_date.blockSignals(True)
            self.transfer_date.setText(formatted)
            self.transfer_date.setCursorPosition(cursor_position + 1)  # 한 개의 '.'을 추가했으므로 커서를 1칸 앞으로 이동
            self.transfer_date.blockSignals(False)

    def update_depositor_name(self, text):
        # 성명 필드의 텍스트를 예금주 필드로 복사
        self.depositor_name.setText(text)
        
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