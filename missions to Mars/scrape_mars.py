from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import os
import time
import pymongo

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    url = 'https://mars.nasa.gov/news/'
    # visit nasa news
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

#parse for titles and article teaser text
    titles = soup.find_all('div', class_='content_title')
    articles = soup.find_all('div', class_='article_teaser_body')

    article_title = titles[1].text.strip()
    article_text = articles.text.strip()

    #append to dict
    mars_dict['article_title'] = article_title
    mars_dict['article_text'] = article_text

    