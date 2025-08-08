import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.init_db()
        self.init_table()
        self.show()
        
        # 버튼 이벤트 연결
        self.btnAdd.clicked.connect(self.add_product)
        self.btnUpdate.clicked.connect(self.update_product)
        self.btnDelete.clicked.connect(self.delete_product)
        self.btnSearch.clicked.connect(self.search_product)
        self.tableWidget.itemClicked.connect(self.select_product)

    def setup_ui(self):
        """UI 구성"""
        # 창 설정
        self.setWindowTitle("전자제품 관리 시스템")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #ddd;
                selection-background-color: #e3f2fd;
                selection-color: #000;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
            }
        """)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 제목 레이블 추가
        title_label = QLabel("전자제품 관리 시스템")
        title_label.setStyleSheet("""
            font-size: 24px;
            color: #1565C0;
            margin-bottom: 20px;
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 입력 폼 구성
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        form_layout = QGridLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(15)

        # ID 입력
        self.label1 = QLabel("제품 ID:")
        self.txtId = QLineEdit()
        self.txtId.setEnabled(False)
        self.txtId.setStyleSheet("background-color: #f5f5f5;")
        form_layout.addWidget(self.label1, 0, 0)
        form_layout.addWidget(self.txtId, 0, 1)

        # 제품명 입력
        self.label2 = QLabel("제품명:")
        self.txtName = QLineEdit()
        form_layout.addWidget(self.label2, 1, 0)
        form_layout.addWidget(self.txtName, 1, 1)

        # 가격 입력
        self.label3 = QLabel("가격:")
        self.txtPrice = QLineEdit()
        form_layout.addWidget(self.label3, 2, 0)
        form_layout.addWidget(self.txtPrice, 2, 1)

        layout.addWidget(form_widget)

        # 버튼 구성
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(10)
        
        self.btnAdd = QPushButton("추가")
        self.btnUpdate = QPushButton("수정")
        self.btnDelete = QPushButton("삭제")
        self.btnSearch = QPushButton("검색")
        
        # 삭제 버튼 스타일 변경
        self.btnDelete.setStyleSheet("""
            background-color: #f44336;
        """)
        
        button_layout.addWidget(self.btnAdd)
        button_layout.addWidget(self.btnUpdate)
        button_layout.addWidget(self.btnDelete)
        button_layout.addWidget(self.btnSearch)
        button_layout.addStretch()
        
        layout.addWidget(button_widget)

        # 테이블 위젯
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        layout.addWidget(self.tableWidget)

    def init_db(self):
        """데이터베이스 초기화"""
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MyProducts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
        
    def init_table(self):
        """테이블 위젯 초기화"""
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['ID', '제품명', '가격'])
        self.load_products()
        
    def load_products(self):
        """제품 목록 불러오기"""
        self.cursor.execute("SELECT * FROM MyProducts")
        products = self.cursor.fetchall()
        
        self.tableWidget.setRowCount(len(products))
        for i, product in enumerate(products):
            for j, value in enumerate(product):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
                
    def add_product(self):
        """제품 추가"""
        name = self.txtName.text()
        price = self.txtPrice.text()
        
        if not name or not price:
            QMessageBox.warning(self, '경고', '모든 필드를 입력하세요.')
            return
            
        try:
            price = int(price)
            self.cursor.execute("INSERT INTO MyProducts (name, price) VALUES (?, ?)",
                              (name, price))
            self.conn.commit()
            self.load_products()
            self.clear_inputs()
        except ValueError:
            QMessageBox.warning(self, '경고', '가격은 숫자로 입력하세요.')
            
    def update_product(self):
        """제품 수정"""
        id = self.txtId.text()
        name = self.txtName.text()
        price = self.txtPrice.text()
        
        if not all([id, name, price]):
            QMessageBox.warning(self, '경고', '모든 필드를 입력하세요.')
            return
            
        try:
            price = int(price)
            self.cursor.execute("UPDATE MyProducts SET name=?, price=? WHERE id=?",
                              (name, price, id))
            self.conn.commit()
            self.load_products()
            self.clear_inputs()
        except ValueError:
            QMessageBox.warning(self, '경고', '가격은 숫자로 입력하세요.')
            
    def delete_product(self):
        """제품 삭제"""
        id = self.txtId.text()
        if not id:
            QMessageBox.warning(self, '경고', '삭제할 제품을 선택하세요.')
            return
            
        reply = QMessageBox.question(self, '확인', '정말로 삭제하시겠습니까?',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM MyProducts WHERE id=?", (id,))
            self.conn.commit()
            self.load_products()
            self.clear_inputs()
            
    def search_product(self):
        """제품 검색"""
        name = self.txtName.text()
        if not name:
            self.load_products()
            return
            
        self.cursor.execute("SELECT * FROM MyProducts WHERE name LIKE ?",
                          ('%' + name + '%',))
        products = self.cursor.fetchall()
        
        self.tableWidget.setRowCount(len(products))
        for i, product in enumerate(products):
            for j, value in enumerate(product):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
                
    def select_product(self, item):
        """테이블에서 선택한 제품 정보를 입력 필드에 표시"""
        row = item.row()
        self.txtId.setText(self.tableWidget.item(row, 0).text())
        self.txtName.setText(self.tableWidget.item(row, 1).text())
        self.txtPrice.setText(self.tableWidget.item(row, 2).text())
        
    def clear_inputs(self):
        """입력 필드 초기화"""
        self.txtId.clear()
        self.txtName.clear()
        self.txtPrice.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())