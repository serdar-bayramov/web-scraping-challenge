from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
from webdriver_manager.firefox import GeckoDriverManager


def scrape():
    browser = Browser('firefox', executable_path=GeckoDriverManager().install(), headless=False)

    news_url = 'https://redplanetscience.com/'
    image_url = 'https://spaceimages-mars.com'
    mars_url = 'https://galaxyfacts-mars.com'
    hem_url = 'https://marshemispheres.com/'

    browser.visit(news_url)
    news_html = browser.html

    # Create BeautifulSoup object and parse with 'html.parser'
    news_soup = BeautifulSoup(news_html,'html.parser')
    titles = news_soup.find_all('div', class_='content_title')
    news_title = titles[0].text
    

    paragraphs = news_soup.find_all('div', class_='article_teaser_body')
    news_p = paragraphs[0].text
    

    browser.visit(image_url)
    image_html = browser.html

    
    # Create BeautifulSoup object and parse with 'html.parser'
    image_soup = BeautifulSoup(image_html, 'html.parser')
    image = image_soup.find("img", class_="thumbimg")["src"]
    img_url = "https://spaceimages-mars.com/" + image
    featured_img_url = img_url

    mars_tables = pd.read_html(mars_url)
    df = mars_tables[1]
    df.columns = ['Description','Data values']
    html_table = df.to_html()
    

    browser.visit(hem_url)
    hem_html = browser.html

    hem_soup = BeautifulSoup(hem_html,'html.parser')
    
    title = hem_soup.find_all('img',attrs={'class':'thumb'})

    hem_list = []
   
    for i in title:
        title = i.attrs['alt']
        img_url = i.attrs['src']
        hem_list.append({'title':title,'imgs_url': hem_url + img_url})

    
    mars_dtb = {
        'news_title':news_title,
        'news_p':news_p,
        'featured_img_url': featured_img_url,
        'html_table': html_table,
        'hem_list': hem_list}
    
    browser.quit()
    return mars_dtb
   
