import requests
import pandas as pd
import json
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
        COLUMNS = ["UNODC_NO", "Title", "YEAR", "Country", "Summary", "Keywords", "Procedural_Fields", "Procedural_Text", "Victims", "Defendants",
                   "Charges"]

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
        if title == "404 Error":
            self.set_url(self.url.replace("migrantsmugglingcrimetype","moneylaunderingcrimetype"))
        title = self.get_title()
        if title == "404 Error":
            self.set_url(self.url.replace("moneylaunderingcrimetype","cybercrimecrimetype"))
        title = self.get_title()
        print(self.url)


        year = self.url.split("/")[-2]
        country = self.get_country()
        unodc_no = self.get_unodc_no()
        summary = self.get_summary()
        keyword_dict = self.get_keywords()
        procedural_dict, procedural_text = self.get_procedural_info()
        victims = self.get_victims()
        defendants = self.get_defendants()
        charges = self.get_charges()

        dataframe = pd.DataFrame([[unodc_no, title, year, country, summary, keyword_dict, procedural_dict, procedural_text, victims,
                                   defendants, charges]], columns=COLUMNS)

        return dataframe, self.url


    def get_title(self):
        title  = self.html.find("title")
        return title.text if title else None

    def get_unodc_no(self):
        decisionDate = self.html.find("div", {"class", "decisionVerdictDate field line"})
        return decisionDate.find("div",{"class":"value"}).text if decisionDate else None

    def get_country(self):
        country_flag = self.html.find("div", {"class":"country icon flip pull-left vcenter"})
        return country_flag.find("span", {"class": "text"}).text if country_flag else None

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
                keyword_dict[label].append(tag.text.strip())
        return keyword_dict if keywords else None

    def get_procedural_info(self):
        procedural_dict = {}
        procedures = self.html.find("div", {"class": "procedural-history"})
        procedure_text = ""
        if not procedures:
            return (None, "")

        keywords = procedures.find_all("div")
        for keyword in keywords:
            label = keyword.find("div", {"class": "label"})
            value = keyword.find("div", {"class": "value"})
            if label:
                label = label.text.replace(":", "")
                procedural_dict[label] = value.text.strip()
            elif keyword.get("class") and "proceduralHistoryDescription" in keyword.get("class"):
                procedure_text = " ".join([x.text for x in keyword.find_all("p")])
        return (procedural_dict, procedure_text) if keywords else (None, "")

    def get_people(self, className):
        victim_list = []
        victims = self.html.find("div", {"class": className})
        if not victims:
            return None
        for victim in victims.find_all("div", {"class":"person"}):
            victim_dict = {}
            for keyword in victim.find_all("div"):
                label = keyword.find("div", {"class": "label"})
                value = keyword.find("div", {"class": "value"})
                paragraphs = " ".join([x.text for x in keyword.find_all("p")])
                if label and value:
                    label = label.text.replace(":", "").replace("\n", "")
                    victim_dict[label.strip()] = value.text.strip() + paragraphs.strip()


            victim_list.append(victim_dict)

        return victim_list

    def get_victims(self):
        return self.get_people("victimsPlaintiffs")

    def get_defendants(self):
        return self.get_people("defendantsRespondents")

    def get_charges(self):
        return self.get_people("charges")

