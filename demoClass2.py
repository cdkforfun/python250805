# 개발자 클래스를 정의
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

    def __repr__(self):
        return f"Person(id={self.id}, name='{self.name}')"
    
#인스턴스를 2개 생성
dev1 = Person(1, "홍길동")
dev2 = Person(2, "김철수")  

# 정보 출력
dev1.printInfo()
dev2.printInfo()    