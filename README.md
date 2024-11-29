# 사전 조건
- python3 설치 필요
- 필수 lib 필요 ( 나중에 작성 )

# catalog를 받아서 catalog/*.html 로 저장
```
cp .env.sample .env
- .env에 reinvent 계정 정보 변경
python3 parsing_pro.py
```
# catalog 파일을 가공하기
## 내가 신청한 항목만 출력하기 
```
- find_catalog.py 파일에 아래 내용을 주석 풀기 ( # 제거 )
    ##### 단건
    # list = ["NTA304-R", "MAM316-R", "ARC322", "KEY002", "STG316", "EUC206", "AIM368", "KUB303-R1", "KUB402-R1", "KEY004", "TLC303-R1", "KUB305-R1", "KUB308", "PEX402-R1"]
    # main("KUB305-R1")

- 실행 명령어
python3 find_catalog.py | tee hcseo.txt

Result) hcseo.txt 에 내용 저장
```

## 전체 항목에 대해서 출력하기
```
- find_catalog.py 파일에 아래 내용을 주석 풀기 ( # 제거 )
    # 파일 저장
    # catalog_dir = "catalog"
    # list = [f.split('.')[0] for f in os.listdir(catalog_dir) if f.endswith('.html')]
    # for catalog in list:
    #     session_info = main(catalog)

- 실행 명령어
python3 find_catalog.py | tee all.txt

Result) all.txt 에 내용 저장
```

## 전체 항목에 대해서 excel로 저장하기
```
- find_catalog.py 파일에 아래 내용을 주석 풀기 ( 현재 제거 상태 )

    # file 저장
    # Excel 저장
    catalog_dir = "catalog"
    list = [f.split('.')[0] for f in os.listdir(catalog_dir) if f.endswith('.html')]
    for catalog in list:
        session_info = main(catalog)
        # Convert session_info to DataFrame if it's the first iteration
        if 'df' not in locals():
            df = pd.DataFrame([session_info])
        else:
            # Append the new session_info to existing DataFrame
            df = pd.concat([df, pd.DataFrame([session_info])], ignore_index=True)

    # After the loop ends, save DataFrame to Excel
    output_file = 'session_catalog.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Session information has been saved to {output_file}")

- 실행 명령어
python3 find_catalog.py | tee all.txt

Result) session_catalog.xlsx 파일 생성
```
