#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 00:11:54 2021

@author: tiffanyelle
"""

from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    # create dict that we can insert into mongo
    mars_data = {}
    
    '''NASA Mars News'''
    # Visit the following URL
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    time.sleep(4)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #News Title
    news_title = soup.find_all('div', class_="content_title")[1].text
    
    #Paragraph Text
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text
    
    mars_data['news_title'] = news_title
    mars_data['news_para'] = news_p

    
    
    browser.quit()
    
    return (mars_data)

print(scrape())