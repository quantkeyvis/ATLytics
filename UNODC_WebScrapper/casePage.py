import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

class CasePage:


    def __init__(self, url):
        self.url = url
        text = requests.get(url).text
        self.html = bs(text, 'html.parser')

    def set_url(self, url):
        self.url = url
        text = requests.get(url).text
        self.html = bs(text, 'html.parser')

    def get_all_data(self):
        COLUMNS = ["Title", "UNODC_NO", "Summary", "Keywords"]

        title = self.get_title()

        if title == "404 Error":
            self.set_url(self.url.replace("traffickingpersonscrimetype","criminalgroupcrimetype"))
        title = self.get_title()
        if title == "404 Error":
            self.set_url(self.url.replace("criminalgroupcrimetype","drugCrimetype"))
        title = self.get_title()
        if title == "404 Error":
            self.set_url(self.url.replace("drugCrimetype","migrantsmugglingcrimetype"))
        title = self.get_title()

        print(self.url)

        unodc_no = self.get_unodc_no()
        summary = self.get_summary()
        keyword_dict = self.get_keywords()

        dataframe = pd.DataFrame([[title, unodc_no, summary, keyword_dict]], columns=COLUMNS)


        return dataframe


    def get_title(self):
        title  = self.html.find("title")
        return title.text if title else None

    def get_unodc_no(self):
        decisionDate = self.html.find("div", {"class", "decisionVerdictDate field line"})
        return decisionDate.find("div",{"class":"value"}).text if decisionDate else None

    def get_summary(self):
        summary = self.html.find("div", {"class": "factSummary"})
        if summary:
            summaryP = summary.find("p")
            if summaryP:
                return summaryP.text
            else:
                return summary.text
        else:
            return None

    def get_keywords(self):
        keyword_dict = {}
        keywords = self.html.find_all("div", {"class": "keywordCategory field"})
        for keyword in keywords:
            label = keyword.find("div", {"class": "label"}).text.replace(":", "")
            keyword_dict[label] = []
            tags = keyword.find_all("div", {"class": "tags"})
            for tag in tags:
                keyword_dict[label].append(str(tag.text))
        return keyword_dict if keywords else None