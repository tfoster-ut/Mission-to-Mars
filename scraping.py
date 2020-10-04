
# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and save results in dictionary
    data = { 
        data_1: {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now()},
        data_2: {
            {"img_url": ce_img_link, "title": ce_img_title},
            {"img_url": sc_img_link, "title": sc_img_title},
            {"img_url": sy_img_link, "title": sy_img_title},
            {"img_url": va_img_link, "title": va_img_title}}

    # Stop webdriver and return data
    browser.quit()
    
    return data


# # Set executable path and initialize Chrome browser
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path)

def mars_news(browser):

    # Visit Mars Nasa Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_not_present_by_css("ul.item_list li.slide", wait_time=1)

    # Setup HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')


    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # This line of code looks inside the slide.elem and specificall identifies the "div and class"
        slide_elem.find("div", class_="content_title")
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
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
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one("figure.lede a img").get("src")
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'http://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    try:
        ### Mars Facts
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    return df.to_html(classes="table table-striped")

def hemisphere():
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Retrieve images and titels from hemispheres
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

    return ce_img_link, ce_img_title, sc_img_link, sc_img_title, sy_img_link, sy_img_title, va_img_link, va_img_title

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
