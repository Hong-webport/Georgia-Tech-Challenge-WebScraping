
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time
# app = Flask(__name__)


def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)




    browser.is_element_present_by_css('.content_title', wait_time=1000) # using wait_time
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # news_title = soup.find('div', class_='list_text').find('div', class_='content_title').text
    news_title_contatiner = soup.find('div', class_='list_text')

    news_title =news_title_contatiner.find('div', class_='content_title').text

    news_p = soup.find('div', class_='list_text').find('div', class_='article_teaser_body').text




    # news_p


    sec_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(sec_url)



    browser.is_element_present_by_css('.carousel_item', wait_time=1000) # using wait_time
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #the link that we have came in  <article alt="Daybreak at Gale Crater" class="carousel_item" style="background-image: url('/spaceimages/images/wallpaper/PIA14293-1920x1200.jpg');">
    featured_image_url = soup.find('article', class_='carousel_item')['style']
    #the result of ['style'] is "background-image: url('/spaceimages/images/wallpaper/PIA14293-1920x1200.jpg');"
    featured_image_url =featured_image_url.replace('background-image: url(', '').replace(');', '')    
    # "'/spaceimages/images/wallpaper/PIA16021-1920x1200.jpg'" is the result of the replace function
    featured_image_url=featured_image_url.replace("'","")
    # '/spaceimages/images/wallpaper/PIA16021-1920x1200.jpg'is the string result we want
    featured_image_url='https://www.jpl.nasa.gov/'+featured_image_url
    #'https://www.jpl.nasa.gov/' is the name of the website assuming the url is correct it gaves the correct after test it out
    # featured_image_url





    # mars Fact
    thr_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(thr_url)
    mars_df=tables[0]
    # mars_df




    frt_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.is_element_present_by_css('.itemLink product-item', wait_time=10) # using wait_time
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')
    # # .find bring only the FIRST RESULT. .Find_all bring out a list
    # imgpage_url = soup.find_all('a', class_='itemLink product-item')



    img_ls=[]
    title_ls=[]
    hemisphere_image_urls=[]

    for i in range(0, 4):
    #   to reinitialize similar to y=0
        browser.visit(frt_url)

        mars_clicks=browser.find_by_css('a.product-item h3', wait_time=1000) # using wait_time
        mars_clicks[i].click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        titles_hem =soup.find('h2', class_='title').text
        title_ls.append(titles_hem)
        
        imgpage_url =soup.find('img', class_='wide-image')['src']
        img_ls.append('https://astrogeology.usgs.gov'+imgpage_url)
        
        mars_dict = dict(title=title_ls[i], img_url=img_ls[i])
        hemisphere_image_urls.append(mars_dict)

    print(hemisphere_image_urls)
    mars_datatalists ={}
    mars_datatalists = {"news_title": news_title,"news_content":news_p,
        "image_url":featured_image_url,
        "mars_table":mars_df.to_html(classes = 'table table-striped', index=False, index_names=False),
            "hemisphere_image_urls": hemisphere_image_urls}
    return mars_datatalists
    # print(mars_datatalists)


# from flask_pymongo import PyMongo
# import scrape_craigslist

# @app.route("/")
# def index():
#     listings = mongo.db.listings.find_one()
#     return render_template("index.html", listings=listings)


# # @app.route("/scrape")
# # def scrap():
# #     listings = mongo.db.listings
# #     listings_data = scrape_craigslist.scrape()
# #     listings.update({}, listings_data, upsert=True)
# #     return redirect("/", code=302)




# if __name__ == "__main__":
#     app.run(debug=True)