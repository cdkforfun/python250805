import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import Workbook

def get_stock_info():
    try:
        url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        print("웹 페이지 요청 중...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        print("HTML 파싱 중...")
        soup = BeautifulSoup(response.text, "html.parser")
        
        # HTML 내용 확인
        print("HTML 내용:", soup.prettify()[:500])  # 처음 500자만 출력

        table = soup.find("table", class_="type_1")
        if not table:
            print("테이블을 찾을 수 없습니다.")
            return []

        stocks = []
        rows = table.find_all("tr")
        print(f"총 {len(rows)}개의 행을 찾았습니다.")

        for row in rows:
            try:
                cols = row.find_all("td")
                if len(cols) >= 7:  # 7개 이상으로 수정
                    link = cols[0].find('a')
                    if not link:
                        continue
                    
                    code = link['href'].split('=')[-1]
                    name = cols[0].get_text(strip=True)
                    
                    # 데이터 확인용 출력
                    print(f"\n처리 중인 종목: {name}")
                    
                    price = cols[1].get_text(strip=True).replace(',', '')
                    
                    # 전일비 처리 수정
                    change_text = cols[2].get_text(strip=True)
                    # 숫자만 추출
                    change = ''.join(filter(str.isdigit, change_text))
                    # 부호 확인
                    is_negative = '하락' in change_text
                    change = int(change) * (-1 if is_negative else 1)
                    
                    rate = cols[3].find('span').get_text(strip=True)
                    volume = cols[4].get_text(strip=True).replace(',', '')
                    amount = cols[5].get_text(strip=True).replace(',', '')
                    marketcap = cols[6].get_text(strip=True).replace(',', '')
                    
                    stock_data = {
                        "종목코드": code,
                        "종목명": name,
                        "현재가": int(price),
                        "전일비": change,  # 이미 int로 변환됨
                        "등락률": rate,
                        "거래량": int(volume),
                        "거래대금": int(amount),
                        "시가총액": int(marketcap)
                    }
                    
                    stocks.append(stock_data)
                    print(f"'{name}' 종목 정보 추가 성공")
                    
            except Exception as e:
                print(f"데이터 처리 중 오류 발생 ({name}): {str(e)}")
                continue

        print(f"총 {len(stocks)}개의 종목 정보를 가져왔습니다.")
        return stocks

    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")
        return []

if __name__ == "__main__":
    print("프로그램 시작...")
    stock_list = get_stock_info()
    
    if stock_list:
        print("\n=== 수집된 종목 정보 ===")
        for stock in stock_list:
            try:
                print(f"\n[{stock['종목코드']}] {stock['종목명']}")
                print(f"현재가: {stock['현재가']:,}원")
                print(f"전일비: {stock['전일비']:,}원 ({stock['등락률']})")
                print(f"거래량: {stock['거래량']:,}")
                print(f"시가총액: {stock['시가총액']:,}억원")
                print("-" * 50)
            except Exception as e:
                print(f"출력 중 오류 발생: {str(e)}")
                
        # 엑셀 파일로 저장
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "코스피200"
            
            # 헤더 추가
            headers = ["종목코드", "종목명", "현재가", "전일비", "등락률", "거래량", "거래대금", "시가총액"]
            ws.append(headers)
            
            # 데이터 추가
            for stock in stock_list:
                row = [
                    stock['종목코드'],
                    stock['종목명'],
                    stock['현재가'],
                    stock['전일비'],
                    stock['등락률'],
                    stock['거래량'],
                    stock['거래대금'],
                    stock['시가총액']
                ]
                ws.append(row)
            
            # 열 너비 자동 조정
            for column in ws.columns:
                max_length = 0
                column = list(column)
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column[0].column_letter].width = adjusted_width
            
            # 파일 저장
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_filename = f"코스피200_{current_time}.xlsx"
            wb.save(excel_filename)
            print(f"\n데이터가 '{excel_filename}' 파일로 저장되었습니다.")
            
        except Exception as e:
            print(f"엑셀 파일 저장 중 오류 발생: {str(e)}")
    else:
        print("데이터를 가져오는데 실패했습니다.")