# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
from splinter.exceptions import ElementDoesNotExist

def start_browser():
    # !which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def Scrap_Mars_data():
    # You must define the output variable
    results_for_mars = {}

    browser=start_browser()
    
    ### NASA Mars News

    url = 'https://mars.nasa.gov/news/'
    response=browser.visit(url)
    
    # Create BeautifulSoup object; parse with 'html'
    html = browser.html 
    
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Examine the results, then determine the element that contains your information
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    clean_title=news_title.strip()
    clean_p=news_p.strip()
    # Run only if title, paragraph are available
    if (news_title and news_p):
        # Print results
        print(clean_title)
        print(clean_p)

        Mars_News = {
        'title': clean_title,
        'Teaser': clean_p
        }
        results_for_mars["Mars_News"]= Mars_News

    ### JPL Mars Space Images - Featured Image
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup_2 = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    image = soup_2.find('div', class_="carousel_items")

    # Clean to get the Url
    dirty_url = image.find('article')['style']
    front_num=dirty_url.find("('")
    back_num=dirty_url.find("')")
    par_image=dirty_url[front_num+len("('"):back_num]

    #Clean the orginal URL
    back_num_2=url_2.find("/s")
    url_2_short=url_2[:back_num_2]

    #Combine the URL for Wallpaper image
    featured_image_url=url_2_short + par_image
    results_for_mars["featured_image_url"]= featured_image_url

    ### Mars Weather

    #Find the latest weather by NASA's Mars twitter account
    url_tweet = 'https://twitter.com/marswxreport?lang=en'
    response_2 = requests.get(url_tweet)
   
    # Create BeautifulSoup object; parse with 'html'
    soup_3 = BeautifulSoup(response_2.text, 'html.parser')
    mars_weather = soup_3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    results_for_mars["mars_weather"]= mars_weather
   

    # Find fun facts
    # URL
    url_facts = 'http://space-facts.com/mars/'
    
    # Pull in HTML table 1
    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['Category', 'Units']
    df = df.set_index("Category")
    df_html = df.to_html()
    df_html_clean= df_html.replace('\n', '')

    results_for_mars["fun_facts"]= df_html_clean
    
    # Mars Hemispheres Scrape
    url_hem ='http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hem)
    html = browser.html
    soup_4 = BeautifulSoup(html, 'html.parser')

    sidebar = soup_4.find_all('div', class_='description')
    # Clean and retreive the Url
    hemisphere_image_urls = []
    work_around_main = 'http://web.archive.org'
    for article in sidebar:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        urls= article.find('a')['href']
        urls_full= work_around_main+urls
        title=article.find('h3').text
        print(urls_full)
        print(title)
        print('---------')
        browser.visit(urls_full)
        html = browser.html
        soups_in_soups = BeautifulSoup(html, 'html.parser')
        #     print(soups_in_soups.prettify())
        downloads = soups_in_soups.find('div', class_='downloads')
        img_url = downloads.find('a')['href']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    results_for_mars["hemisphere_image_urls"]= hemisphere_image_urls

      # Close the browser after scraping
    browser.quit()
    return results_for_mars