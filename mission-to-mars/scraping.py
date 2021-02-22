from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
import time

def scrape_all():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': hem_facts(browser)
    }



    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    
    slide_elem = news_soup.select_one("ul.item_list li.slide")
    # Use the parent element to find the first 'a' tag and save it as 'news_title'
    news_title = slide_elem.find("div", class_="content_title").get_text()
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
        

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():

    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
        
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    return df.to_html()

def hem_facts(browser):
    base_url = 'https://astrogeology.usgs.gov'
    search_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(search_url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    thumbsoup = img_soup.find_all('img', class_='thumb')
    link_mess = img_soup.find_all('a', class_='itemLink product-item')

    hemisphere_image_assets = []
    linkfilter = []

    for title in thumbsoup:
        hem_elems = {}
        hem_elems['title'] = title.get('alt')
        
        for branch in link_mess:
            link = branch.get('href')
            
            #filter duplicates
            if link not in linkfilter:      
                linkfilter.append(link)
                browser.visit(f'{base_url}{link}')
                time.sleep(1.5)
                html = browser.html
                detail_soup = soup(html, 'html.parser')
                imglink = detail_soup.find('li')
                truepath = imglink.a['href']
                hem_elems['img_url'] = truepath
                hemisphere_image_assets.append(hem_elems)
                browser.back()

    
                    
    browser.quit    
    return(hemisphere_image_assets)

if __name__ == "__main__":
    print(scrape_all())