import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic
import sqlite3
import os.path

# 데이터베이스 관련 클래스
class ProductDatabase:
    def __init__(self, db_name="ProductList.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """DB 연결 및 테이블 생성"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            if not os.path.exists(self.db_name):
                self.create_table()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "데이터베이스 오류", f"데이터베이스 연결 실패: {str(e)}")

    def __del__(self):
        """소멸자: DB 연결 해제"""
        if self.connection:
            self.connection.close()

    def create_table(self):
        """Products 테이블 생성"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Price INTEGER
            );
        """)
        self.connection.commit()

    def add_product(self, name, price):
        """제품 추가"""
        try:
            if not name or not price:
                raise ValueError("제품명과 가격을 모두 입력하세요")
            price = int(price)
            if price < 0:
                raise ValueError("가격은 0보다 커야 합니다")
            self.cursor.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (name, price))
            self.connection.commit()
            return True
        except ValueError as e:
            QMessageBox.warning(None, "입력 오류", str(e))
            return False
        except sqlite3.Error as e:
            QMessageBox.critical(None, "데이터베이스 오류", str(e))
            return False

    def update_product(self, id, name, price):
        """제품 수정"""
        self.cursor.execute("UPDATE Products SET Name=?, Price=? WHERE id=?;", (name, price, id))
        self.connection.commit()

    def remove_product(self, id):
        """제품 삭제"""
        self.cursor.execute("DELETE FROM Products WHERE id=?;", (id,))
        self.connection.commit()

    def get_products(self):
        """모든 제품을 가져오기"""
        self.cursor.execute("SELECT * FROM Products;")
        return self.cursor.fetchall()

# UI 관련 클래스
class DemoForm(QMainWindow, uic.loadUiType("Chap10_ProductList.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # ProductDatabase 객체 생성
        self.db = ProductDatabase()

        # QTableWidget 초기 설정
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        self.tableWidget.setTabKeyNavigation(False)
        
        # 초기 데이터 로드
        self.getProduct()
        
        # 이벤트 연결
        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())
        self.tableWidget.doubleClicked.connect(self.doubleClick)

    def addProduct(self):
        """새 제품 추가"""
        name = self.prodName.text().strip()
        price = self.prodPrice.text().strip()
        
        if self.db.add_product(name, price):
            self.getProduct()
            self.clearInputFields()

    def updateProduct(self):
        """제품 수정"""
        try:
            id = self.prodID.text().strip()
            name = self.prodName.text().strip()
            price = self.prodPrice.text().strip()
            
            if not all([id, name, price]):
                raise ValueError("모든 필드를 입력하세요")
                
            if self.db.update_product(id, name, price):
                self.getProduct()
                self.clearInputFields()
                
        except ValueError as e:
            QMessageBox.warning(self, "입력 오류", str(e))

    def removeProduct(self):
        """제품 삭제"""
        try:
            id = self.prodID.text().strip()
            if not id:
                raise ValueError("제품 ID를 선택하세요")
                
            reply = QMessageBox.question(self, '삭제 확인', 
                '정말로 이 제품을 삭제하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
            if reply == QMessageBox.Yes:
                self.db.remove_product(id)
                self.getProduct()
                self.clearInputFields()
                
        except ValueError as e:
            QMessageBox.warning(self, "입력 오류", str(e))

    def getProduct(self):
        """모든 제품을 테이블에 표시"""
        try:
            products = self.db.get_products()
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(products))
            
            for row, item in enumerate(products):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(item[0])))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(item[1]))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(item[2])))
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "데이터베이스 오류", str(e))

    def clearInputFields(self):
        """입력 필드 초기화"""
        self.prodID.clear()
        self.prodName.clear()
        self.prodPrice.clear()
        self.prodName.setFocus()

    def doubleClick(self, item):
        """테이블 더블클릭 시 선택된 행의 데이터를 입력 필드에 표시"""
        row = item.row()
        self.prodID.setText(self.tableWidget.item(row, 0).text())
        self.prodName.setText(self.tableWidget.item(row, 1).text())
        self.prodPrice.setText(self.tableWidget.item(row, 2).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm()
    demoForm.show()
    app.exec_()
