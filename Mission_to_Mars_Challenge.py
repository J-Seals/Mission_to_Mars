#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')


# In[5]:


slide_elem = news_soup.select_one('div.list_text')


# In[6]:


slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[15]:


df.to_html()


# In[16]:


#browser.quit()


# In[17]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[18]:


html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
#cerberus_url_rel = img_soup.find('a', target='_blank').get('href')
#cerberus_url_rel


# In[20]:


#cerberus_img = browser.links.find_by_text("Sample").first
#cerberus_img


# In[21]:


imgs_ = browser.find_by_css("a.product-item img")
imgs_

for i in range(len(imgs_)):
    hemispheres = {}
    
    #Get image
    browser.find_by_css("a.product-item img")[i].click()
    cerberus_img = browser.links.find_by_text("Sample").first
    hemispheres["img_url"] = cerberus_img["href"]
    
    #Get title
    hemispheres["img_title"] = browser.find_by_css("h2.title").text
    
    #Call dictionary into empty list
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# In[22]:


#cerberus_img["href"]


# In[23]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[24]:


# 5. Quit the browser
browser.quit()


# In[ ]:




