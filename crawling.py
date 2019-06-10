from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def get_naver_news_content(url):
    html = urlopen(url)
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, 'lxml', from_encoding='utf-8')
    title = soup.findAll('div', {'id':'main_content'})[0].findAll('div', {'class':'article_info'})[0].find('h3',{'id':'articleTitle'}).text
    main_text = soup.findAll('div', {'id':'articleBodyContents'})[0].get_text(" ", strip=True)
    main_text = main_text[63:]
    
    return title, main_text  # title : 기사의 제목, main_text : 기사의 본문

def get_naver_news_list(pages=1, date='20190610'):
    base_url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001&listType=title&date=' + date + '&page='
    urls = []
    for page in range(1, pages + 1):
        print('load {} page'.format(page))
        res = requests.get(base_url + str(page))
        res.raise_for_status()
        res.encoding = None
        html = res.text

        soup = BeautifulSoup(html, 'html.parser')
        news_block_list = soup.find('div', {'class':'list_body newsflash_body'}).findAll('ul', {'class':'type02'})

        for news_block in news_block_list:
            news_list = news_block.findAll('li')
            for news in news_list:
                urls.append(news.find('a').get('href'))
    
    return urls







