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
    
    
    '''JPL Mars Space Images - Featured Image'''
    # Visit the following URL
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    featured_image_url = soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = url.replace("index.html","") + featured_image_url
    mars_data['featured_image'] = featured_image_url

    '''Mars Facts'''
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    
    #Slicing off other dataframes
    df = tables[0]
    df = df.rename(columns={0: "Description", 1: "Mars"})
    df = df.set_index(['Description'])
    
    #Pandas dataframe to html
    #html_table = df.to_html() 
  
    #strip unwanted newlines to clean up the table
    #html_table.replace('\n', '')
       
    
    
    browser.quit()
    
    return (mars_data,df)

print(scrape())



























































