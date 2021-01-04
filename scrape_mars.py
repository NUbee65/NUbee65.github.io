#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 20:59:21 2021

@author: brook
"""

#%% Dependencies

import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo


#%% Configure ChromeDriver / Setup Splinter

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


#%% NASA Mars News

def mars_news():
    
    for i in range(0,4):
        while True:
            try:
        
                url = 'https://mars.nasa.gov/news'
                browser.visit(url)

                html = browser.html
                news_soup = BeautifulSoup(html, 'html.parser')

                article_container = news_soup.find('ul', class_='item_list')

                article_date = article_container.find('div', class_='list_date').text
                article_title = article_container.find('div', class_='content_title').text
                article_summary = article_container.find('div', class_='article_teaser_body').text.strip()
    
            except Exception as e:
                print(e)
            break
    
    return article_date, article_title, article_summary


#%% JPL Space Images - Featured Image

def featured_image():
    
    for i in range(0,4):
        while True:
            try:    
    
                url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
                browser.visit(url)

                html = browser.html
                featured_image_soup_1 = BeautifulSoup(html, 'html.parser')

                featured_image_title = featured_image_soup_1.find('h1', 'media_feature_title').text.strip()

                featured_image_element_m1 = featured_image_soup_1.find('article', class_='carousel_item')['style']
                image_url_m1 = featured_image_element_m1.replace("background-image: url('", '')
                image_url_m1 = image_url_m1.replace("');", '')
                image_url_m1 = f'https://www.jpl.nasa.gov{image_url_m1}'
                featured_image_url = image_url_m1

            except Exception as e:
                print(e)
            break                
                
    return featured_image_title, featured_image_url


#%% Mars Facts

def mars_facts():

    for i in range(0,4):
        while True:
            try:

                url = 'https://space-facts.com/mars/'
                browser.visit(url)

                mars_facts_df = pd.read_html(url)
                mars_facts_df = mars_facts_df[0]
                mars_facts_df.columns = ['Planet Metric', 'Mars']

                mars_facts_html = mars_facts_df.to_html(classes='table table=striped', index=False, justify='left', border=0)

            except Exception as e:
                print(e)
            break  

    return mars_facts_html


#%% Mars Hemispheres

def mars_hemispheres():

    for i in range(0,4):
        while True:
            try:
    
                # Initiate empty list of dictionaries (no dictionaries yet present)
                global hemisphere_image_urls
                hemisphere_image_urls = []

                # URL of page to be scraped and Configure Splinter
                # URL = universal resource locator (FYI)
                url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
                browser.visit(url)

                # Capture HTML from URL
                html = browser.html

                # Get list of hemispheres 
                links = browser.find_by_css("a.product-item h3")

                # Traverse Splinter links
                for i in range(len(links)):

                    #Find the elements on each loop 
                    browser.find_by_css("a.product-item h3")[i].click()

                    # Capture HTML from second URL (linked page)
                    html = browser.html

                    # Parse HTML from second URL (linked page) with BeautifulSoup
                    mars_hemispheres_image_soup = BeautifulSoup(html, 'html.parser')

                    # Use BeautifulSoup to zero in on image_title
                    mars_hemispheres_image_title = mars_hemispheres_image_soup.find('h2', class_='title').text

                    # Use BeautifulSoup to zero in on relative URL for wide_image (full image)
                    mars_hemispheres_image_url = mars_hemispheres_image_soup.find('img', class_='wide-image')['src']

                    # Augment relative URL to create full URL for wide_image (full image)
                    mars_hemispheres_image_url = 'https://astrogeology.usgs.gov' + mars_hemispheres_image_url

                    # Initiate empty dictionary
                    hemisphere_dict = {}

                    # Populate dictionary with results
                    hemisphere_dict = {"title": mars_hemispheres_image_title, "img_url": mars_hemispheres_image_url}

                    # Append dictionary to list of dictionaries
                    hemisphere_image_urls.append(hemisphere_dict)

                    # Use Splinter to go back to prior web page
                    browser.back()

            except Exception as e:
                print(e)
            break  
            
    return hemisphere_image_urls


#%% Function to Scrape All Data

def scrape_all():
    article_date, article_title, article_summary  = mars_news()
    featured_image_title, featured_image_url = featured_image()
    mars_facts_html = mars_facts()
    hemisphere_image_urls = mars_hemispheres()
    
    global mars_dict    
    
    mars_dict = {
        'article_date': article_date, 
        'article_title': article_title,
        'article_summary': article_summary,
        'featured_image_title': featured_image_title, 
        'featured_image_url': featured_image_url,
        'mars_facts_html': mars_facts_html,
        'hemisphere_image_urls': hemisphere_image_urls
    }
    
    # print(mars_dict)
    
    return mars_dict






