class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

    def __repr__(self):
        return f"Person(id={self.id}, name='{self.name}')"

class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Title: {self.title}")

    def __repr__(self):
        return f"Manager(id={self.id}, name='{self.name}', title='{self.title}')"

class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")

    def __repr__(self):
        return f"Employee(id={self.id}, name='{self.name}', skill='{self.skill}')"

# 테스트 코드
def test_person():
    p = Person(1, "홍길동")
    print(p)
    assert p.id == 1
    assert p.name == "홍길동"

def test_person_printInfo(capsys):
    p = Person(2, "김철수")
    p.printInfo()
    captured = capsys.readouterr()
    print(captured.out.strip())
    assert "ID: 2, Name: 김철수" in captured.out

def test_manager():
    m = Manager(3, "이영희", "팀장")
    print(m)
    assert m.id == 3
    assert m.name == "이영희"
    assert m.title == "팀장"

def test_manager_printInfo(capsys):
    m = Manager(4, "박민수", "부장")
    m.printInfo()
    captured = capsys.readouterr()
    print(captured.out.strip())
    assert "ID: 4, Name: 박민수, Title: 부장" in captured.out

def test_employee():
    e = Employee(5, "최수진", "Python")
    print(e)
    assert e.id == 5
    assert e.name == "최수진"
    assert e.skill == "Python"

def test_employee_printInfo(capsys):
    e = Employee(6, "정우성", "Java")
    e.printInfo()
    captured = capsys.readouterr()
    print(captured.out.strip())
    assert "ID: 6, Name: 정우성, Skill: Java" in captured.out

def test_manager_is_person():
    m = Manager(7, "김지훈", "과장")
    print(m)
    assert isinstance(m, Person)

def test_employee_is_person():
    e = Employee(8, "이서연", "C++")
    print(e)
    assert isinstance(e, Person)

def test_manager_inheritance():
    m = Manager(9, "한지민", "팀장")
    print(m)
    assert hasattr(m, "id") and hasattr(m, "name") and hasattr(m, "title")

def test_employee_inheritance():
    e = Employee(10, "박지성", "SQL")
    print(e)
    assert hasattr(e, "id") and hasattr(e, "name") and hasattr(e, "skill")