import os
import argparse
import crawling
import textrank
import pandas as pd

if __name__ == '__main__':
    titles = []
    contents = []
    date = '20190610'
    news_urls = crawling.get_naver_news_list(date=date)
    for news_url in news_urls:
        title, content = crawling.get_naver_news_content(news_url)
        titles.append(title)
        contents.append(content)

    news_title_dataset = pd.DataFrame()
    news_title_dataset['title'] = titles
    news_title_dataset['content'] = contents
    news_title_dataset['url'] = news_urls
    news_title_dataset.set_index("url")
    news_title_dataset.to_csv('news_dataset_'+date + '.csv')
    
    for content in contents[:5]:
        print(textrank.summarize(content))