from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from make_text_file import MakeTextFile
import pandas as pd
import os

chromedriver_autoinstaller.install()

url = "https://aws.amazon.com/about-aws/whats-new/2024/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-categories=*all"
# https://aws.amazon.com/about-aws/whats-new/2024/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-categories=*all&awsm.page-whats-new-content-all=2
last_page=23

def is_correct_date(date):
    date_list = date.split("/")
    month = int(date_list[0])
    day = int(date_list[1])
    year = int(date_list[2])
    if month >= 12:
        return True
    elif month == 11 and day >= 23:
        return True
    return False

def find_page(page, driver, category):
    time.sleep(5)
    print(f"find_page start {page}")
    try:
        # 페이지 로딩 대기
        catalog_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.aws-directories-container-wrapper"))
        )
        # 카탈로그 컨테이너 요소 대기
        # catalog_container = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.aws-directories-container-wrapper"))
        # )
        
        # li 항목들 찾기
        li_items = catalog_container.find_elements(By.CSS_SELECTOR, "ul.aws-directories-container > li")
        
        print(f"총 {len(li_items)}개의 li 항목을 찾았습니다.")
            
        count = 1
        news_list = []
        # 각 li 항목 처리 (예: 텍스트 출력)
        for item in li_items:
            try:
                # # 세션 ID 추출
                # session_id = item.get_attribute('id')
                
                # # 세션 제목 추출
                title_element = item.find_element(By.CSS_SELECTOR, 'div.m-card-title')
                if title_element:
                    title = title_element.text 
                else: 
                    title = f"제목 없음"

                link_element = item.find_element(By.CSS_SELECTOR, 'div.m-card-title > a')
                if link_element:
                    link = link_element.get_attribute('href')
                else: 
                    link = f"링크 없음"
                
                date_element = item.find_element(By.CSS_SELECTOR, 'div.m-card-info')
                if date_element:
                    date = date_element.text 
                else: 
                    date = f"날짜 없음"
                session_info = {
                    'Category': category,
                    'Title': title,
                    'Link': link,
                    'Date': date
                }
                print(title, link, date)
                news_list.append(session_info)
            except Exception as e:
                print(f"항목 처리 중 오류 발생: {e}")
                return []
        return news_list
            
    except Exception as e:
        print(f"li 항목을 찾는 중 오류 발생: {e}")



def main():
    category_list = [
        ["Analytics", "analytics"],
        ["Application Integration", "application-services"],
        ["Blockchain", "blockchain"],
        ["Business Applications", "business-productivity"],
        ["Cloud Financial Management", "cost-management"],
        ["Compute", "compute"],
        ["Containers", "containers"],
        ["Customer Enablement", "customer-enablement"],
        ["Customer Engagement", "messaging"],
        ["Database", "databases"],
        ["Developer Tools", "developer-tools"],
        ["End User Computing", "desktop-and-app-streaming"],
        ["Front End Web & Mobile", "mobile-services"],
        ["GameTech", "game-development"],
        ["Internet of Things", "internet-of-things"],
        ["Machine Learning", "artificial-intelligence"],
        ["Management & Governance", "management-and-governance"],
        ["Media Services", "media-services"],
        ["Migration and Transfer", "migration"],
        ["Networking & Content Delivery", "networking-and-content-delivery"],
        ["Partners", "aws-marketplace-and-partners"],
        ["Quantum Technologies", "quantum-technologies"],
        ["Robotics", "robotics"],
        ["Satellite", "satellite"],
        ["Security, Identity, & Compliance", "security-identity-and-compliance"],
        ["Serverless", "serverless"],
        ["Storage", "storage"],
        ["Training and Certification", "training-and-certification"]
    ]
    # Set up Chrome options for English language
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    
    # Set number of pages to scrape
    last_page = 17
    driver = webdriver.Chrome(options=options)

    session_list = []
    for category_info in category_list:
        for page in range(1, last_page):
            url=f"https://aws.amazon.com/about-aws/whats-new/2024/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-categories=marketing-marchitecture%23{category_info[1]}&awsm.page-whats-new-content-all={page}"
            driver.get(url)
            time.sleep(5)
            blog_list = find_page(page, driver, category_info[0])
            if blog_list:
                if is_correct_date(blog_list[0]['Date']) == False:
                    break
                for blog_info in blog_list:
                    session_list.append(blog_info)
            else:
                break
        for session_info in session_list:
            print(session_info)
            if 'df' not in locals():
                df = pd.DataFrame([session_info])
            else:
                # Append the new session_info to existing DataFrame
                df = pd.concat([df, pd.DataFrame([session_info])], ignore_index=True)
    output_file = 'news_catalog.xlsx'
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    # 메인 함수 호출
    main()