#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Sewt executable path and initialize Chrome browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


# Visit Mars Nasa Site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_not_present_by_css("ul.item_list li.slide", wait_time=3)


# In[6]:


# Setup HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem


# In[7]:


# This line of code looks inside the slide.elem and specificall identifies the "div and class"
slide_elem.find("div", class_="content_title")


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_="content_title").get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[10]:


# Visit URL
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_id("full_image")
full_image_elem.click()


# In[12]:


# Find the more info button and click that
browser.is_element_present_by_text("more info", wait_time=1)
more_info_elem = browser.links.find_by_partial_text("more info")
more_info_elem.click()


# In[13]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, "html.parser")


# In[14]:


# Find the relative image url
img_url_rel = img_soup.select_one("figure.lede a img").get("src")
img_url_rel


# In[15]:


# Use the base URL to create an absolute URL
img_url = f'http://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[16]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[17]:


df.to_html()


# ### Mars Weather

# In[18]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[19]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[20]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# In[ ]:





# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[21]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[22]:


# 2. Create a list to hold the images and titles.

# 3. Write code to retrieve the image urls and titles for each hemisphere.
ce_click = browser.links.find_by_partial_text("Cerberus")
ce_click.click()

html = browser.html
ce_img = soup(html, 'html.parser')
ce_img_link = ce_img.find("div", class_="wide-image-wrapper")
ce_img_link = ce_img_link.find_all("a")[0].get("href")
ce_img_title = ce_img.title.get_text()
browser.back()

sc_click = browser.links.find_by_partial_text("Schiaparelli")
sc_click.click()

html = browser.html
sc_img = soup(html, 'html.parser')
sc_img_link = sc_img.find("div", class_="wide-image-wrapper")
sc_img_link = sc_img_link.find_all("a")[0].get("href")
sc_img_title = sc_img.title.get_text()
browser.back()

sy_click = browser.links.find_by_partial_text("Syrtis")
sy_click.click()

html = browser.html
sy_img = soup(html, 'html.parser')
sy_img_link = sy_img.find("div", class_="wide-image-wrapper")
sy_img_link = sy_img_link.find_all("a")[0].get("href")
sy_img_title = sy_img.title.get_text()
browser.back()

va_click = browser.links.find_by_partial_text("Valles")
va_click.click()

html = browser.html
va_img = soup(html, 'html.parser')
va_img_link = va_img.find("div", class_="wide-image-wrapper")
va_img_link = va_img_link.find_all("a")[0].get("href")
va_img_title = va_img.title.get_text()

hemisphere_image_urls = [
    {"img_url": ce_img_link, "title": ce_img_title},
    {"img_url": sc_img_link, "title": sc_img_title},
    {"img_url": sy_img_link, "title": sy_img_title},
    {"img_url": va_img_link, "title": va_img_title}
]


# In[24]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[25]:


# 5. Quit the browser
browser.quit()


# In[ ]:




