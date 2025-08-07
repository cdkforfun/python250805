# web1.py
# 크롤링 작업
from bs4 import BeautifulSoup

#페이지를 로딩
page = open('Chap09_test.html', 'rt', encoding='utf-8')

# 검색이 용이한 객체
soup = BeautifulSoup(page, 'html.parser')
# 전체 문서 보기
# print(soup.prettify())

#<p> 전체 검색
# print(soup.find_all('p'))
# <p> 태그 중 첫 번째 검색
# print(soup.find('p'))  
# 특정 스타일: <p class="outer-text">
print(soup.find_all('p', class_='outer-text'))
# id 속성: <p id="first">
print(soup.find_all('p', id='first'))   
# 태그 내부의 문자열만 추출: .text, .get_text()
for tag in soup.find_all('p'):
    title = tag.text.strip()  # 양쪽 공백 제거
    title = title.replace('\n', '')  # 줄바꿈 제거
    print(title)


