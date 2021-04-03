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
#--------------------------
    #begin scrape for jpl images website
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = bs(html, 'html.parser')

    #Go to featured images
    browser.links.find_by_partial_text('FULL IMAGE').click()
    image = jpl_soup.find('img', class_='headerimage fade-in')
    jpl_image = image['src']

    jpl_image_url = jpl_url + jpl_image
#--------------------------------
    facts_url="https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    #rename columns and index table
    tables[0].columns = ['Description', 'Mars']
    tables[0].set_index('Description', inplace=True)
    #Back to Html
    mars_facts_html = tables[0].to_html()
    mars_facts_html.replace('\n', '')

#--------------------------------

#usgs site 

    baseurl = 'https://astrogeology.usgs.gov'
    astro_url = baseurl + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(astro_url)