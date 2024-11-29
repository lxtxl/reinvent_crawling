import os
from bs4 import BeautifulSoup
import pandas as pd
   
def get_title(soup, html_tag, class_name, title):
    time_location_element = soup.find(f"{html_tag}", {"class": f"{class_name}"})
    if time_location_element:
        time_info = time_location_element.text
        time_info = time_info.replace("\n", " ")
        time_info = ' '.join(time_info.split())
        return f"{time_info}"
    else:
        return "{title} 정보를 찾을 수 없습니다."

def get_speaker(soup, html_tag, class_name, title, child_tag):
    # speaker-details
    time_location_element = soup.find(f"{html_tag}", {"class": f"{class_name}"})
    sentence = "스피커 ------------"
    if time_location_element:
        find_p = time_location_element.find_all("p")
        for speaker in find_p:
            speaker_info = speaker.text
            speaker_info = speaker_info.replace("\n", " ")
            speaker_info = ' '.join(speaker_info.split())
            sentence = sentence + "\n" + speaker_info
        sentence = sentence + "\n" + "--------------"
        return f"{sentence}"
    else:
        return "{title} 정보를 찾을 수 없습니다."
def main(catalog):
    html_file_path = f"catalog/{catalog}.html"

    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')
    # 시간 정보 추출
    date = get_title(soup, "span", "session-date", "날짜")
    time = get_title(soup, "span", "session-time", "시간")
    # time = time.replace("12:00 PM", "12:00")
    # time = time.replace("12:30 PM", "12:30")
    # time = time.replace("11:00 PM", "23:00")
    # time = time.replace("11:30 PM", "23:30")
    # time = time.replace("10:00 PM", "22:00")
    # time = time.replace("10:30 PM", "22:30")
    # time = time.replace("9:00 PM", "21:00")
    # time = time.replace("9:30 PM", "21:30")
    # time = time.replace("8:00 PM", "20:00")
    # time = time.replace("8:30 PM", "20:30")
    # time = time.replace("7:00 PM", "19:00")
    # time = time.replace("7:30 PM", "19:30")
    # time = time.replace("6:00 PM", "18:00")
    # time = time.replace("6:30 PM", "18:30")
    # time = time.replace("5:00 PM", "17:00")
    # time = time.replace("5:30 PM", "17:30")
    # time = time.replace("4:00 PM", "16:00")
    # time = time.replace("4:30 PM", "16:30")
    # time = time.replace("3:00 PM", "15:00")
    # time = time.replace("3:30 PM", "15:30")
    # time = time.replace("2:00 PM", "14:00")
    # time = time.replace("2:30 PM", "14:30")
    # time = time.replace("1:00 PM", "13:00")
    # time = time.replace("1:30 PM", "13:30")
    print("=" * 30)
    print(f"{date} {time}")

    title = get_title(soup, "div", "title-text", "타이틀")
    print(f"{title}")
    location = get_title(soup, "span", "session-location", "위치")
    print(f"{location}")
    hotel = location.split('|')[0]
    session_type = get_title(soup, "div", "rf-session-types", "세션타입")
    print(f"{session_type}")
    topic = get_title(soup, "div", "attribute-Topic", "topic")
    print(f"topic: {topic}")
    inderstry = get_title(soup, "div", "attribute-Industry", "Industry")
    print(f"Industry: {inderstry}")
    interest = get_title(soup, "div", "attribute-Areaofinterest", "interest")
    print(f"{interest}")
    level = get_title(soup, "div", "attribute-Level", "level")
    print(f"{level}")
    role = get_title(soup, "div", "attribute-Role", "role")
    print(f"{role}")
    services = get_title(soup, "div", "attribute-Services", "service")
    print(f"{services}")
    speaker = get_speaker(soup, "div", "speaker-details", "speaker", "p")
    print(f"{speaker}")
    print("=" * 30)
    # Create a dictionary to store the session information
    session_info = {
        'Date': date,
        'Time': time,
        'Title': title,
        'Hotel': hotel,
        'Location': location,
        'Session Type': session_type,
        'Topic': topic,
        'Industry': inderstry,
        'Area of Interest': interest,
        'Level': level,
        'Role': role,
        'Services': services
    }
    
    # Return the session info dictionary to be collected
    return session_info

if __name__ == "__main__":
    ##### 단건
    # list = ["NTA304-R", "MAM316-R", "ARC322", "KEY002", "STG316", "EUC206", "AIM368", "KUB303-R1", "KUB402-R1", "KEY004", "TLC303-R1", "KUB305-R1", "KUB308", "PEX402-R1"]
    # main("KUB305-R1")

    # 파일 저장
    # catalog_dir = "catalog"
    # list = [f.split('.')[0] for f in os.listdir(catalog_dir) if f.endswith('.html')]
    # for catalog in list:
    #     session_info = main(catalog)

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
