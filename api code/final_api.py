from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.request import urlopen
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

app = FastAPI()

def price_amzn(key):
    

    response_amazon = urlopen("https://www.amazon.in/s?k=" + key.replace(' ','+'))

    bs_amazon = BeautifulSoup(response_amazon,'lxml')

    pdt_amazon = bs_amazon.find_all('div',{'data-component-type':'s-search-result'})

    result_map = []

    base_url = 'https://www.amazon.in'

    sleep(10)

    for i in pdt_amazon:

        name=i.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).get_text()

        try:
            price = i.find('span',{'class':'a-price-whole'}).get_text()
        except AttributeError as e:
            price = "N/A"

        try:
            link = i.find('a',{'class':'a-link-normal s-no-outline'}).get("href")
        except AttributeError as e:
            link = "N/A"
        
        try:
            img_link = i.find('img',{'class':'s-image'}).get('src')
        except AttributeError as e:
            img_link = "N/A"

        try:
            rating = i.find('i',{'class':'a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom'}).get_text()
        except AttributeError as e:
            rating = "N/A"

        result_map.append({'name' : name,'price' : price,'link' : base_url + link,'image_link' : img_link,'rating' : rating[0:3]})

    return result_map

@app.get("/search_amazon/")
def search_amazon(key: str):
    if key:
        result = price_amzn(key)
        return result
    else:
        raise HTTPException(status_code=400, detail="Please provide a 'key' parameter.")
    
def price_flipkart(key):
    
    path = 'C://Users//arora//Desktop//api pracitce//chromedriver'

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Create a WebDriver with the specified options
    browser = webdriver.Chrome(options=chrome_options)



    browser.get('https://www.flipkart.com/')

    browser.minimize_window()

    input_search = browser.find_element(By.CLASS_NAME, 'Pke_EE')
    search_button = browser.find_element(By.CLASS_NAME, '_2iLD__')
    pop_up_close = browser.find_element(By.CLASS_NAME, '_30XB9F')

    sleep(2)
    pop_up_close.click()

    input_search.send_keys(key)
    sleep(2)
    search_button.click()

    result_map = []
    
    for i in range(1):
        # print('Scraping page', i+1)
        parent_cards = browser.find_elements(By.CLASS_NAME,'_13oc-S')

       

        for parent_card in parent_cards :
            product = parent_card.find_element(By.CLASS_NAME, '_4rR01T')
            price = parent_card.find_element(By.CSS_SELECTOR, '._30jeq3._1_WHN1')
            link = parent_card.find_element(By.CLASS_NAME, '_1fQZEK')
            rating = parent_card.find_element(By.CLASS_NAME, '_3LWZlK')
            image_link = parent_card.find_element(By.CLASS_NAME,'_396cs4')
            # image_link =
        
            result_map.append({'name' : product.text,'price' : price.text, 'link' : link.get_attribute("href"), 'rating' : rating.text,'image_link' : image_link.get_attribute("src")})
            # print(price[i])
        # print(len(price),len(product),len(link))
        # next_button = browser.find_element(By.XPATH, "//a[text()='Next']")
        # next_button.click()
        # sleep(5)
    
    browser.close()
    
    return result_map

@app.get("/search_flipkart/")
def search_flipkart(key: str):
    if key:
        result = price_flipkart(key)
        return result
    else:
        raise HTTPException(status_code=400, detail="Please provide a 'key' parameter.")
    

def price_jiomart(key):
    
    path = 'C://Users//arora//Desktop//api pracitce//chromedriver'

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Create a WebDriver with the specified options
    browser = webdriver.Chrome(options=chrome_options)



    browser.get('https://www.jiomart.com/')

    browser.minimize_window()

    input_search = browser.find_element(By.CSS_SELECTOR, '.aa-Input.search_input')
    
    input_search.send_keys(key)
    input_search.send_keys(Keys.ENTER)

    sleep(7)

    result_map = []
    
    for i in range(1):
        # print('Scraping page', i+1)
        parent_cards = browser.find_elements(By.CSS_SELECTOR,'.ais-InfiniteHits-item.jm-col-4.jm-mt-base')
        # print(parent_cards)
        # sleep(100)
        base_url = 'https://www.jiomart.com/'
        for parent_card in parent_cards :
            product = parent_card.find_element(By.CSS_SELECTOR, '.plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80')
            price = parent_card.find_element(By.CSS_SELECTOR, '.jm-heading-xxs.jm-mb-xxs')
            link = parent_card.find_element(By.CSS_SELECTOR, '.plp-card-wrapper.plp_product_list')
            rating = ''
            image_link = parent_card.find_element(By.TAG_NAME, 'img')
            # # image_link =
            # print(image_link.get_attribute("src"))
            result_map.append({'name' : product.text,'price' : price.text, 'link' : link.get_attribute("href"), 'rating' : rating,'image_link' : image_link.get_attribute("src")})
            # print(price[i])
        # print(len(price),len(product),len(link))
        # next_button = browser.find_element(By.XPATH, "//a[text()='Next']")
        # next_button.click()
        # sleep(5)
    
    browser.close()
    
    return result_map

@app.get("/search_jiomart/")
def search_jiomart(key: str):
    if key:
        result = price_jiomart(key)
        return result
    else:
        raise HTTPException(status_code=400, detail="Please provide a 'key' parameter.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
