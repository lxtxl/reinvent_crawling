import os
import time
from googletrans import Translator
from bs4 import BeautifulSoup
import sys
import requests
import pandas as pd

url = "https://aws.amazon.com/ko/blogs/aws/"
# https://aws.amazon.com/ko/blogs/aws/page/2/

def get_article(soup, html_tag, class_name, title):
    time_location_element = soup.find(f"{html_tag}", {"class": f"{class_name}"})
    if time_location_element:
        time_info = time_location_element.text
        time_info = time_info.replace("\n", " ")
        time_info = ' '.join(time_info.split())
        return f"{time_info}"
    else:
        return "{title} 정보를 찾을 수 없습니다."

def get_url(soup, html_tag, class_name, title):
    time_location_element = soup.find(f"{html_tag}", {"class": f"{class_name}"})
    if time_location_element:
        link_element = time_location_element.find("a")
        if link_element and 'href' in link_element.attrs:
            return link_element['href']
    return "URL을 찾을 수 없습니다."

def get_span(soup, html_tag, class_name, filter, title):
    time_location_element = soup.select(f"{html_tag}.{class_name} > span")
    if time_location_element:
        for row in time_location_element:
            if filter in row.text:
                return row.text.strip()
    return f"{title}을 찾을 수 없습니다."

def get_blog_title(soup):
    return get_article(soup, "h2", "blog-post-title", "title")
    
def get_blog_link(soup):
    return get_url(soup, "h2", "blog-post-title", "title")

def get_blog_speaker(soup):
    return get_span(soup, "footer", "blog-post-meta", "by", "speaker")
    
def get_blog_date(soup):
    return get_span(soup, "footer", "blog-post-meta", "on", "date")    

def get_blog_tag(soup):
    return get_span(soup, "footer", "blog-post-meta", "in", "tag")    

def get_blog_explain(soup):
    return get_article(soup, "section", "blog-post-excerpt", "explain")

def find_page(page):
    if page == 1:
        url = "https://aws.amazon.com/ko/blogs/aws/"
    else:
        url = f"https://aws.amazon.com/ko/blogs/aws/page/{page}/"
    # Send HTTP GET request to the URL
    response = requests.get(url)
    
    blog_list = []
    # Check if request was successful
    if response.status_code == 200:
        # Get the page content
        html = response.text
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
        return
    soup = BeautifulSoup(html, 'html.parser')
    #aws-page-content-main > article:nth-child(2) > div > div.lb-col.lb-mid-18.lb-tiny-24 > h2 > a
    working_list = soup.find_all("article", {"class": "blog-post"})

    for row in working_list:  # 첫 번째 행은 헤더이므로 제외
        print("=" * 30)
        title = get_blog_title(row)
        print(title)
        url_link = get_blog_link(row)
        print(url_link)
        speaker = get_blog_speaker(row)
        print(speaker)
        date = get_blog_date(row)
        print(date)
        tag = get_blog_tag(row)
        print(tag)
        explain = get_blog_explain(row)
        print(explain)
        session_info = {
            'Title': title,
            'Url': url_link,
            'Speker': speaker,
            'Date': date,
            'Tag': tag,
            'Explain': explain
        }
        blog_list.append(session_info)
    return blog_list
    
    
def main(page):
    session_list = []
    for page in range(1, 11):
        blog_list = find_page(page)
        if blog_list:
            for blog_info in blog_list:
                session_list.append(blog_info)

    for session_info in session_list:
        print(session_info)
        if 'df' not in locals():
            df = pd.DataFrame([session_info])
        else:
            # Append the new session_info to existing DataFrame
            df = pd.concat([df, pd.DataFrame([session_info])], ignore_index=True)
    output_file = 'blog_catalog.xlsx'
    df.to_excel(output_file, index=False)
        

if __name__ == "__main__":
        # Check if exactly one parameter is provided
    if len(sys.argv) == 2:
        page = int(sys.argv[1])
        main(page)
    else:
        for page in range(1, 11):
            main(page)
