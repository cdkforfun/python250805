# demoFunction.py

#1) 함수를 정의
def setValue(newValue):
    # 지역변수
    x = newValue
    print("함수내부:", x)

#2) 함수를 호출
retValue = setValue(5)
print(retValue)

#1) 함수를 정의
def swap(x,y):
    return y,x

#2) 함수를 호출
result = swap(3,4)
print(result)


print("---함수이름해석---")
x=5
def func(a):
    return a+x

print(func(1))

def func2(a):
    x=10
    return a+x
print(func2(1))

print("---기본값---")
def times(a=10, b=20):
    return a*b
print(times())
print(times(5))
print(times(5,6))

def connectURI(server,port):
    strURL = "https://" + server + ":" + port
    return strURL

print(connectURI("multi.com", "80"))
print(connectURI(port = "80", server = "test.com"))