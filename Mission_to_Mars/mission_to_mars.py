#!/usr/bin/env python
# coding: utf-8

# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():

	executable_path = {'executable_path': '/usr/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)

# Create dictionary for returning mars information after scraping
mars_info = {}

# Mars Data Scraping from NASA News Page


def scrape_mars_news():
	try:
		#initialize browser
		browser = init_browser()
		
		# Set URL to NASA Mars News website
		news_url = 'https://mars.nasa.gov/news/'
		browser.visit(news_url)
		time.sleep(5)

		# Create HTML Object and parse HTML with Beautiful Soup
		html_news = browser.html
		soup = BeautifulSoup(html_news, 'html.parser')

		
		# Scrape data from the title and p tags
		text_tag = soup.find('div', class_='list_text')
		title = text_tag.find('div', class_='content_title')
		article_title = title.find('a').text
		article_p = soup.find('div', class_='article_teaser_body').text

		# Append dictionary entry from Mars News Source
        	mars_info['news_title'] = article_title
        	mars_info['news_paragraph'] = article_p
		
		return mars_info
	
	finally:
	
		browser.quit()
	


# Mars Image Scraping from JPL Page
def scrape_mars_image():

	try:
	
		#initialize browser
		browser = init_browser()
		
		# Set URL to JPL website
		image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
		image_url_prefix = 'https://jpl.nasa.gov'
		browser.visit(image_url_featured)
		time.sleep(5)


		# Create HTML Object and parse HTML with Beautiful Soup 
		html_image = browser.html
		soup = BeautifulSoup(html_image, 'html.parser')
		
		#retrieve background image url from style tag
		image_carousel = soup.find('article', class_='carousel_item')
		footer = image_carousel.find('footer')
		link_url = footer.find('a')["data-fancybox-href"]
		
		# concat website url with scraped route
		featured_image_url = image_url_prefix + link_url
		
		# display featured image
		featured_image_url

		# dictionary entry from featured image
		mars_info['featured_image_url'] = featured_image_url
		
		return mars_info
	
	finally:
		
		browser.quit()
		
		
# Mars Data Scraping from Mars Facts Page
def scrape_mars_facts():

	# Set URL to Mars Facts website
	facts_url = 'http://space-facts.com/mars/'

	# Parse the URL using Pandas
	mars_facts = pd.read_html(facts_url)
	

	# Find the table containing the Mars Facts and assign it to mars_df
	mars_df = mars_facts[0]

	# Label the columns
	mars_df.columns = ['Description','Value']

	# Reassign index to the `Description` column
	mars_df.set_index('Description', inplace=True)

	# Save html code
	data = mars_df.to_html()
	
	# dictionary entry from MARS FACTS
	mars_info['mars_facts'] = data
	
	return mars_info


# Mars Hemisphere Image Scraping from usgs.gov
def scrape_mars_hemispheres():

	try:

		# initialize browser
		browser = init_browser()
		
		# Set URL to usgs.gov website
		hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
		browser.visit(hemisphere_url)
		time.sleep(5)

		# Create HTML Object and parse HTML with Beautiful Soup
		html_hemisphere = browser.html
		soup = BeautifulSoup(html_hemisphere, 'html.parser')

		# Declare list variables for storing image URLs dictionary
		hemisphere_image_urls = []
		hemisphere_url_prefix = 'https://astrogeology.usgs.gov'

		# Retreive all items that contain Mars Hemispheres data
		items = soup.find_all('div', class_='item')

		# loop through the items
		for i in items: 
		    # Store title
		    title = i.find('h3').text
		    
		    # Store link that leads to full image website
		    partial_img_url = i.find('a', class_='itemLink product-item')['href']
		    
		    # Visit the link that contains the full image website 
		    browser.visit(hemisphere_url_prefix + partial_img_url)
		    
		    # HTML Object of individual hemisphere information website 
		    partial_img_html = browser.html
		    
		    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
		    soup = BeautifulSoup( partial_img_html, 'html.parser')
		    
		    # Retrieve full image source 
		    img_url = hemisphere_url_prefix + soup.find('img', class_='wide-image')['src']
		    
		    # Append the retreived information into a list of dictionaries 
		    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
		
		mars_info['hemisphere_image_urls'] = hemisphere_image_urls
		
		# Return mars_data dictionary
		
		return mars_info
	
	finally:
		
		browser.quit()
