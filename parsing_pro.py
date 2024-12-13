from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from make_text_file import MakeTextFile
import os
from dotenv import load_dotenv

load_dotenv()
user_name=os.environ.get("USER_NAME")
password=os.environ.get("PASSWORD")

chromedriver_autoinstaller.install()
url = "https://registration.awsevents.com/flow/awsevents/reinvent24/sessioncatalog/page/page"

def login_process(driver):
    username_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    #\36 38240e3-f4c3-4e6a-b6c2-4ef22a533f98
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    # 이메일 입력 필드에 이메일 주소 입력
    username_field.send_keys(user_name)
    password_field.send_keys(password)

    time.sleep(5)

    # 로그인 버튼 찾기
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='rf-button-button-login']"))
    )

    # 로그인 버튼 클릭
    login_button.click()

    print("로그인 버튼을 클릭했습니다.")
    time.sleep(30)

def show_more_click_process(driver):
    count = 1
    # show more 버튼 클릭
    while True:
        try:
            # 'Show more' 버튼 찾기
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mdBtnR.mdBtnR-primary.show-more-btn"))
            )
            # 버튼 클릭
            show_more_button.click()
            print(f"{count}번째 'Show more' 버튼을 클릭했습니다.")
            # 페이지 로딩을 위해 잠시 대기
            time.sleep(1)
            count = count + 1
        except:
            print("더 이상 'Show more' 버튼이 없습니다. 모든 콘텐츠를 로드했습니다.")
            break

def extended_click_process(driver):
    count = 1
    # show more 버튼 클릭

    hide_buttons = driver.find_elements(By.XPATH, '//button[@aria-expanded="false" and @aria-label="Session Details"]')

    for hide_button in hide_buttons:
        # 버튼 클릭
        print(hide_button.get_attribute('outerHTML'))
        driver.execute_script("arguments[0].click();", hide_button)
        print(f"{count}번째 'Hide' 버튼을 클릭했습니다.")
        # 페이지 로딩을 위해 잠시 대기
        time.sleep(1)
        count = count + 1


def get_catalog(driver):
    # li 항목들을 찾기 위한 코드
    try:
        # 카탈로그 컨테이너 요소 대기
        catalog_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#rf-catalog > div > main > div:nth-child(3) > div > ul"))
        )
        
        # li 항목들 찾기
        li_items = catalog_container.find_elements(By.TAG_NAME, "li")
        
        print(f"총 {len(li_items)}개의 li 항목을 찾았습니다.")
            
        count = 1
        # 각 li 항목 처리 (예: 텍스트 출력)
        for item in li_items:
            try:
                # # 세션 ID 추출
                # session_id = item.get_attribute('id')
                
                # # 세션 제목 추출
                title_element = item.find_element(By.CSS_SELECTOR, 'div.title-text')
                if title_element:
                    title = title_element.text 
                    split_title = title.split("|")
                    category_title = split_title[0].strip()
                else: 
                    category_title = f"제목 없음 {count}"
                
                if os.path.exists(f"catalog/{category_title}.html"):
                    continue
                html = item.get_attribute('outerHTML')
                
                file = MakeTextFile(f"catalog/{category_title}.html")
                file.writeSave(html)
                print(f"{count}번째 {category_title} 를 파일로 저장했습니다.")
                count = count + 1
                # # 세션 설명 추출
                # description_element = item.find_element(By.CSS_SELECTOR, '.description')
                # description = description_element.text if description_element else "설명 없음"
                
                # # 세션 시간 및 장소 추출
                # time_location_element = item.find_element(By.CSS_SELECTOR, '.rf-session-card-time-location')
                # time_location = time_location_element.text if time_location_element else "시간 및 장소 정보 없음"
                
                # # 배지(태그) 추출
                # badges = item.find_elements(By.CSS_SELECTOR, '.badges .badge')
                # badge_texts = [badge.text for badge in badges]
                
                # print(f"세션 ID: {session_id}")
                # print(f"제목: {title}")
                # print(f"설명: {description}")
                # print(f"시간 및 장소: {time_location}")
                # print(f"배지: {', '.join(badge_texts)}")
                # print("-" * 50)
                # break
            
            except Exception as e:
                print(f"항목 처리 중 오류 발생: {e}")
            
    except Exception as e:
        print(f"li 항목을 찾는 중 오류 발생: {e}")

def main():
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)
    # 로그인 요소 찾기
    login_process(driver)

    show_more_click_process(driver)
    
    extended_click_process(driver)

    get_catalog(driver)

    time.sleep(10)
    print("성공하였습니다.")


if __name__ == "__main__":
    # 메인 함수 호출
    main()
