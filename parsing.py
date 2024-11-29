import pandas as pd
from bs4 import BeautifulSoup
from googletrans import Translator

# Translator 객체 생성
translator = Translator()

html_file_path = 'input.htm'

with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 테이블에서 데이터 추출

working_list = soup.find_all("li", {"class": "catalog-result"})
rows = []
index = 1
for row in working_list:  # 첫 번째 행은 헤더이므로 제외
    # print(">" * 30)
    # print(row.text)
    # print("<" * 30)
    sentence = row.text
    sentence_result = translator.translate(sentence, src='en', dest='ko')
    rows.append([index, row.text, sentence_result])
    # rows.append([index, row.text])
    index = index + 1
    print(index)

# Pandas 데이터프레임으로 변환
df = pd.DataFrame(rows)

# # Excel 파일로 저장
output_excel_path = 'output_translate.xlsx'
df.to_excel(output_excel_path, index=False)

print(f"Excel 파일로 변환이 완료되었습니다: {output_excel_path}")