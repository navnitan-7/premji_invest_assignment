import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse

def fin_get_top_5_search(keyword):
    keyword_quote  = urllib.parse.quote_plus(keyword)
    url = f"https://backend.finshots.in/backend/search/?q={keyword_quote}"
    response = requests.get(url)
    articles=(response.json()['matches'])
    data=[]
    for i in articles[:5]:
        info = {}
        info["url"] = i["post_url"]
        info["title"] = i["title"]
        # info["excerpt"] = i["excerpt"]
        # info["published_date"] = i["published_date"]
        data.append(info)
    df = pd.DataFrame(data)
    df["company"] = keyword
    return df

def fin_get_article_body(url:str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    target_div = soup.find('div', class_="post-content")

    # Extract all text elements in the order they appear
    body = ""

    for element in target_div.find_all(['h1', 'h2', 'h3', 'p', 'span', 'li', 'a']):
        text = element.get_text(strip=True)
        if text:  # Avoid empty strings
            if str.lower("Share this story onWhatsApporTwitter") in str.lower(text):
                break
            body  += "\n" +  text
    body = body.strip()
    return  body