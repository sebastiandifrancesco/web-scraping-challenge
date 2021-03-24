# --- dependencies and setup ---
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time

def init_browser():
    # Set executable path & initialize Chrome browser
    executable_path = {"executable_path": "./chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Visit NASA Mars news site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Parse results HTML using BeautifulSoup
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")
    slide_element.find("div", class_="content_title")
    # Scrape the latest news title
    title = slide_element.find("div", class_="content_title").get_text()
    # Scrape the latest paragraph text
    paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    
    # Visit the NASA JPL Site
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    # Click button with class name full_image
    full_image_button = browser.find_by_xpath("/html/body/div[1]/div/a/button")
    full_image_button.click()
    
    # Parse results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    featured_image_url = image_soup.select_one("body > div.fancybox-overlay.fancybox-overlay-fixed > div > div > div > div > img").get("src")
    # Use base URL to create absolute URL
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"

    # Visit the Mars facts site using pandas
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    html_table = mars_df.to_html(index=False, header=False, border=0, classes="table table-sm table-striped font-weight-light")
    
    # Visit hemispheres website through splinter module 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # HTML object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain Mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_url 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retrieved information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    #  Store all values in dictionary
    scraped_data = {
        "news_title": title,
        "news_para": paragraph,
        "featuredimage_url": featured_image_url,
        "mars_fact_table": html_table, 
        "hemisphere_images": hemisphere_image_urls
    }

    # --- Return results ---
    return scraped_data