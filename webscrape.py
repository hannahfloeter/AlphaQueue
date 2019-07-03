import csv,os,json
import requests

from lxml import html
from time import sleep


def AmazonParser(url):
    #Mac OS X-based computer using a Safari browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    page = requests.get(url,headers=headers)

    while True:

        sleep(3)

        try:
            #doc represents thehtml of the url we requested
            doc = html.fromstring(page.content)

            #xpath found from "inspecting" page on Amazon, using selections of portions of text, or whole groups of nodes to extract
            XPATH_NAME = '//h1[@id="title"]//text()'
            #contains(@id,"ourprice") or contains(@id,"saleprice") or
            XPATH_SALE_PRICE = '//span[contains(@class,"a-color-price")]/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_PAGES = '//ul//li[contains(.,"pages")]/text()'
            XPATH_NUMREV = '//a[@id = "dp-summary-see-all-reviews"]//h2[contains(.,"customer reviews")]/text()'
            XPATH_AVGREV = '//span[@class = "arp-rating-out-of-text a-color-base" and contains(.,"out of 5 stars")]/text()'
            XPATH_IMG_SRC = '//img[@id = "imgBlkFront"]/@data-a-dynamic-image'
            XPATH_DESC = './/div[@data-hook="review-collapsed"]//text()'


            #RAW variables represent the data we scraped from each indiciual path
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_PAGES = doc.xpath(XPATH_PAGES)
            RAW_NUMREV = doc.xpath(XPATH_NUMREV)
            RAW_AVGREV = doc.xpath(XPATH_AVGREV)
            RAW_IMG_SRC = doc.xpath(XPATH_IMG_SRC)
            RAW_DESC = doc.xpath(XPATH_DESC)

            #Making strings out of the raw text along with splitting and cleaning up the data we got a little. THis is where we include checks if nothing was grabbed
            #in which case we retunr a null value for the field.
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            PAGES = ' '.join(''.join(RAW_PAGES).split()) if RAW_PAGES else None
            NUMREV = ' '.join(''.join(RAW_NUMREV).split()) if RAW_NUMREV else None
            AVGREV = ' '.join(''.join(RAW_AVGREV).split()) if RAW_AVGREV else None
            IMG_SRC = ' '.join(''.join(RAW_IMG_SRC).split()) if RAW_IMG_SRC else None
            DESC = ' '.join(''.join(RAW_DESC).split()) if RAW_DESC else None

            #debugging purposees: print out invaild URLs
            if page.status_code!=200:
                print(url)

            #if the URL is blocked then it will return and print NULL in json file
            if NAME == None:
                return None

            #data printed in json file
            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'URL':url,
                    'PAGES':PAGES,
                    'NUMBER OF REVIEWS':NUMREV,
                    'AVERAGE REVIEW': AVGREV,
                    'IMAGE SOURCE:': IMG_SRC,
                    'DESCRIPTION': DESC,
                    }

            return data

        except Exception as e:
            print (e)


def doWebScraping():

    extracted_data = []

    with open('data.csv') as csvfile:
        #reads in file "data.csv"
        input_file = csv.DictReader(csvfile)
        for row in input_file:
            url = "" + str(row['url'])
            #print row
            extracted_data.append(AmazonParser(url))
            sleep(5)

    #creates json file
    f=open('data_test','w')
    json.dump(extracted_data,f,indent=4)


if __name__ == "__main__":
    doWebScraping()
