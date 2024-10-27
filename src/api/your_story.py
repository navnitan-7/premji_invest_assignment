import requests
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

def ys_get_top_5_search(driver, keyword):    
    url = f"https://yourstory.com/search?q={keyword}&page=1"
    driver.get(url)

    # Allow time for the page to load
    time.sleep(5)

    article_elements = driver.find_elements(By.CLASS_NAME, 'sc-43a0d796-0')
    article_urls = []
    for i in article_elements[:10]:
        article_url = (i.get_attribute('href'))
        if article_url not in article_urls:
            article_urls.append(article_url)
    df = pd.DataFrame(article_urls, columns=["url"])
    df["company"] = keyword
    return df


def ys_get_article_body(url:str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    target_div = soup.find('div', id="article_container")
    title_classes = soup.find_all(class_="article-title")

    title = ""
    for title_class  in  title_classes:
        title += " " + title_class.get_text() 

    # Extract all text elements in the order they appear
    body = ""
    for element in target_div.find_all(['h1', 'h2', 'h3', 'p', 'span', 'li', 'a']):
        text = element.get_text(strip=True)
        if text:  # Avoid empty strings
            body  += "\n" +  text
    body=body.strip()
    return title, body