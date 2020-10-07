
# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# Sewt executable path and initialize Chrome browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# Visit Mars Nasa Site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_not_present_by_css("ul.item_list li.slide", wait_time=3)


# Setup HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# This line of code looks inside the slide.elem and specificall identifies the "div and class"
slide_elem.find("div", class_="content_title")


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_="content_title").get_text()


# Use the parent element to find the paragraph text
news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

# ### Featured Images

# Visit URL
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id("full_image")
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text("more info", wait_time=1)
more_info_elem = browser.links.find_by_partial_text("more info")
more_info_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, "html.parser")


# Find the relative image url
img_url_rel = img_soup.select_one("figure.lede a img").get("src")


# Use the base URL to create an absolute URL
img_url = f'http://www.jpl.nasa.gov{img_url_rel}'

# ### Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)


df.to_html()


# ### Mars Weather


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
weather_table.prettify()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
hemi_soup = soup(html, 'html.parser')

# Create empty dict to hold hemisphere links
hemispheres = {}

# Lead url to append to extract
lead_url = "https://astrogeology.usgs.gov"

# Loop through url and obtain extract for each site
for url in hemi_soup.find_all("a", class_="itemLink product-item"):
    url = url.get("href")
    url = lead_url + url
    if url not in hemispheres.keys():
        hemispheres[url]=1

# Convert dict to a list
hemispheres = list(hemispheres.keys())


# 2. Create a list to hold the images and titles.
length = len(hemispheres)
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(length):
    browser.visit(hemispheres[x])
    html = browser.html
    html_soup = soup(html, "html.parser")
    image_link = html_soup.find("div", class_="wide-image-wrapper")
    image_link = image_link.find_all("a")[0].get("href")
    title = html_soup.title.get_text()
    # Append empty list
    hemisphere_image_urls.append({"img_url": image_link, "title": title})
    # Loop iterator
    x += 1

# 5. Quit the browser
browser.quit()


