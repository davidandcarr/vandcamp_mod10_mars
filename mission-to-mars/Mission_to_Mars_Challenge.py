#!/usr/bin/env python
# coding: utf-8

# In[135]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
#scroll way down for step 1


# In[159]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the Quotes to Scrape site
#Seeing that this was an introductory visit, I have overlayed these steps with the heart of the lesson
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#optional wait (why?)
#I get it now
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[12]:


# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')
slide_elem = html_soup.select_one('ul.item_list li.slide')


# In[17]:


slide_elem.find('div', class_='content_title').text


# In[19]:


#searching parent -> para
news_p = slide_elem.find('div', class_='article_teaser_body').text
news_p


# In[15]:


news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[16]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# In[ ]:





# In[20]:


# Visit new URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[23]:


full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[24]:


#parse the soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[27]:


img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[29]:


img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[ ]:





# In[30]:


#new url
url = 'http://space-facts.com/mars/'
browser.visit(url)


# In[33]:


df = pd.read_html(url)[0]
df.columns=['description','value']
df.set_index('description', inplace=True)
df


# In[34]:


df.to_html()


# In[35]:


browser.quit()


# In[ ]:





# In[9]:


###a holdover from the lesson. Not relevant for this challenge, but the structure will be helpful
#for x in range(1, 6):
#   html = browser.html
#   quote_soup = soup (html, 'html.parser')
#   quotes = quote_soup.find_all('span', class_='text')
#   for quote in quotes:
#      print('page:', x, '----------')
#      print(quote.text)
#   browser.links.find_by_partial_text('Next')


# In[ ]:





# <h1>Begin Challenge Steps</h1>

# In[4]:


#step1 - visiting hemispheres site
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[6]:


html = browser.html
img_soup = soup(html, 'html.parser')


# In[72]:


thumbsoup = img_soup.find_all('img', class_='thumb')
thumbspoon = img_soup.find('img', class_='thumb')


# In[75]:


thumbsoup


# In[109]:


spoon = thumbspoon.get('alt')
spoon


# In[81]:


thumbtitles = []
for img in thumbsoup:
    thumbtitles.append(img.get('alt'))


# In[ ]:


#there we go. found my titles and we can clean it up with regex later i think..
#now to see if we can click links via these titles. otherwise cleanup happens first


# In[105]:


#seeing as we're using dicts and such, what about this mess?
thumb_mess = img_soup.find('div', class_='item')
part = thumb_mess.a['href']
part
#ok we can isolate the link. now let's try clicking and pulling our full url


# In[ ]:


#just a reminder while parsing below
thumb_dump = img_soup.find('div', class_='item')


# In[120]:


browser.find_by_name(f'{text}').first.click()
#i think i need to take "thumbnail" out. boooooo. let me try one more thing


# In[117]:


text = thumb_mess.h3.text
text
#oh i like this. maybe it will work
#narrator voice: it did not
#but at least this is the acceptable format of the deliverable


# In[ ]:


#this works but i can't very well automate it
browser.click_link_by_partial_text('Cerberus')


# In[128]:


#maybe i'm trying too hard. we have a class right there. let's give it a go
link_mess = img_soup.find_all('a', class_='itemLink product-item')
link_mess


# In[ ]:


for branch in link_mess:
    link = branch.get('href')


# In[142]:


#huh ok. let's apply the title iteration to this
link_splat = img_soup.find('a', class_='itemLink product-item')
link_splat


# In[131]:


splat_link = link_splat.get('href')
link_splat.get('href')


# In[133]:


browser.click_link_by_href(f'{splat_link}')
#no go on this one. ok, let's just use a base url, make a full string, then work from there


# In[163]:


#testing before looping like a fool
base_url = 'https://astrogeology.usgs.gov'
search_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(search_url)
html = browser.html
img_soup = soup(html, 'html.parser')
link_mess = img_soup.find_all('a', class_='itemLink product-item')

linkfilter = []

for branch in link_mess:
    link = branch.get('href')
    
    if link not in linkfilter:
        linkfilter.append(link)
        print(f'Visiting {link}')
        time.sleep(3)
        browser.visit(f'{base_url}{link}')
        #pull stuff
        time.sleep(2)
        browser.back()
        
    else:
        print('Duplicate')
#why did it do it twice???
#oh lmao because it is listed a second time in the h3. ok. so what if we do an if/then with the appendages...


# In[165]:


browser.url


# In[166]:


html = browser.html
detail_soup = soup(html, 'html.parser')


# In[167]:


imglink = detail_soup.find('li')
imglink


# In[168]:


imglink.a['href']


# In[5]:


#lists for image urls and titles
image_links = []
image_titles = []


# In[ ]:


#let's think it through..
#oh right. list of dicts
for loop through htmlsheet:
    hem_elems = {}
    hemisphere_image_urls = []
    find 'img' class_'alt' 
    append to hem_elems['title']
    
    #the below is deprecated after testing, but the human language makes sense to me
    for title in image_titles:
        click.link_by_partial_href
        append  'li' class_='href' to image_links
        browser.back()


# In[174]:


#let's bring it all together
base_url = 'https://astrogeology.usgs.gov'
search_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(search_url)
html = browser.html
img_soup = soup(html, 'html.parser')
thumbsoup = img_soup.find_all('img', class_='thumb')
link_mess = img_soup.find_all('a', class_='itemLink product-item')

hemisphere_image_urls = []
linkfilter = []

for title in thumbsoup:
    hem_elems = {}
    hem_elems['title'] = title.get('alt')
    
    for branch in link_mess:
        link = branch.get('href')
        
        #filter duplicates
        if link not in linkfilter:      
            linkfilter.append(link)
            print(f'Visiting {link}')
            browser.visit(f'{base_url}{link}')
            time.sleep(3)
            html = browser.html
            detail_soup = soup(html, 'html.parser')
            imglink = detail_soup.find('li')
            truepath = imglink.a['href']
            print(f'Adding image url')
            hem_elems['img_url'] = truepath
            hemisphere_image_urls.append(hem_elems)
            browser.back()

        else:
            print('Duplicate')    
    
print(hemisphere_image_urls)
        
    


# In[175]:


hemisphere_image_urls


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




