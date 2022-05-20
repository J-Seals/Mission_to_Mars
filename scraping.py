 
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import numpy as np

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


# Run all scraping functions and store results in dictionary
    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemisphere(browser),
      "last_modified": dt.datetime.now()
}
    browser.quit()
    return data

# Setup Splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

     # Add try/except for error handling
    try:
    
        slide_elem = news_soup.select_one('div.list_text')
        # slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p
 

# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

# Add try/except for error handling
    try:  
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe      
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()
    df.to_html()

def hemisphere(browser):
    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
  
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    links = browser.find_by_css("a.product-item img")
    

    for i in range(len(links)):
        hemispheres = {}
       
        # Find elements going to click link.
        browser.find_by_css('.description > a.product-item h3')[i].click()

        # Find sample image link
        element = browser.find_link_by_text('Sample').first

        # Get hemisphere Title
        img_url = element['href']

        title = browser.find_by_css("h2.title").text
        # Get hemisphere Title
        hemispheres["title"] = title
        #hemispheres['title'] = browser.find_by_css('h2.title').text

        # Add Objects to hemisphere_image_urls list
        hemispheres["img_url"] = img_url
        hemisphere_image_urls.append(hemispheres)
        
        browser.back()

    
    return hemisphere_image_urls
    # #browser.quit()
    

if __name__ == "__main__":

# If running as script, print scraped data
    print(scrape_all())



