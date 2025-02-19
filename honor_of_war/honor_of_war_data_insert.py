import pandas as pd
import sqlite3
from PyQt5.QtWidgets import QFileDialog
from data_control import add_from_file
from honor_of_war.honor_of_war_current import show_current

# SQLite3 데이터베이스 연결
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

def select_files(self):
    selected_file, _ = QFileDialog.getOpenFileName(self, '엑셀 파일 선택', '', '엑셀 파일 (*.xlsx *.xls)')
    if selected_file:  # 사용자가 파일을 선택했는지 확인
        insert_from_excel(self, selected_file)


def insert_from_excel(self, file):
    try:
        df = pd.read_excel(file, skiprows=2, dtype=str)

        address_col = next((col for col in df.columns if col.startswith("주") and "주민등록번호" not in col), "주    소")
        
        # 첫 번째 행을 제외하고 데이터 리스트 생성
        data_list = [
            (
                str(row.get("행정동", ""))[3:],  # '01-진잠동' → '진잠동'
                str(row.get("보훈번호", "")),
                str(row.get("성 명", "")).strip(),
                str(row.get("주민등록번호", "")),
                str(row.get(address_col, "")),
                str(row.get("입금유형", "")),
                str(row.get("은행명", "")),
                str(row.get("예금주", "")).strip(),
                str(row.get("계좌번호", "")),
                str(row.get("비고", " "))
            )
            for i, (_, row) in enumerate(df.iterrows()) if i != 0  # 첫 번째 행 제외
        ]

        # 데이터베이스에 일괄 삽입 (Bulk Insert)
        add_from_file(data_list)

        show_current(self)

        print(f"'{file}'의 데이터를 성공적으로 처리했습니다.")
    except Exception as e:
        print(f"파일 '{file}' 처리 중 오류 발생: {e}")
