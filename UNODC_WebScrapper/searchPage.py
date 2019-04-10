from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import pandas as pd
from . import casePage

class SearchPage:

    def __init__(self, search_url="https://sherloc.unodc.org/cld/v3/htms/cldb/search.html?lng=en#?c=%7B%22filters%22:%5B%5D,%22sortings%22:%22%22%7D"):
        self.search_url = search_url

    def get_html(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(30)
        driver.get(self.search_url)

        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return bs(driver.page_source, 'html.parser')

    def get_page_urls(self):
        soup = self.get_html()
        dates = soup.find_all('div', {"class": "pull-right flip date-value ng-binding"})
        titles = soup.find_all("strong", {"class": "ng-binding"})
        title_array = [strong.text.replace(" ", "_").replace("/","") for strong in titles]

        year_array = [div.text.replace('\n', "").replace(',', '').replace(' ', '').split("-")[0]
                      for i, div in enumerate(dates)
                      if i % 2 == 0]

        flags = soup.find_all("img")[2:]
        flag_array = [x.get("src").split(".png")[0].split("/")[-1] for x in flags]

        BASE_URL = "https://sherloc.unodc.org/cld/case-law-doc/traffickingpersonscrimetype"
        target_urls = []
        for title, year, flag in zip(title_array, year_array, flag_array):
            target_urls.append( ("{base}/{flag}/{year}/{title}.html?lng=en&tmpl=htms".format(
                flag=flag, base=BASE_URL, year=year, title=title).replace("///", "/"),
                                 year))

        return target_urls

    def load_urls(self, path):
        urls = []
        with open(path, "r")  as f:
            reader = csv.reader(f, delimiter='|')
            for url in reader:
                urls.append(url[0].lower())
        return urls


    def collect_data(self, urls):

        df = None
        new_urls =[]

        for i, url in enumerate(urls):

            page = casePage.CasePage(url)
            pageData, new_url = page.get_all_data()
            new_urls.append(new_url)
            print(pageData)
            if df is None:
                df = pageData
            else:
                df = pd.concat([df, pageData])

        df.reset_index(inplace=True)
        df.drop("index", axis=1, inplace=True)
        return df, new_urls







