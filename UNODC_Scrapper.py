# -*- coding: utf-8 -*-
import requests
import re
import sys
import csv
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import pickle
from datetime import datetime, timedelta
import math

the_cols=['timestamp','url','inmate_id','inmate_firstname','inmate_lastname','inmate_middlename','inmate_sex','inmate_race','inmate_age','inmate_dob','inmate_address','booking_timestamp','processing_numbers','agency','facility','charges','severity','court_dates','days_jailed','bond_amount','current_status','release_timestamp','other','notes']
##########  Case Pull
# Fill country with names of countries to analyze
country_list=[]
country=r'United States of America'
country=country.replace(' ','%20')
print(country)
r'https://sherloc.unodc.org/cld/v3/htms/cldb/search.html?lng=en#?c=%7B%22filters%22:%5B%7B%22fieldName%22:%22en%23caseLaw@country_label_s%22,%22value%22:%22'+country+r'%22%7D%5D%7D'
stamp=str(datetime.now()).split(" ")
d = str(datetime.today() - timedelta(days=3)).split(" ")[0]
full_time=stamp[1]
stamp=stamp[0]
full_time=full_time.split(".")[0]
full_time=full_time.replace(":","-")

r = requests.get(url_site)
dfs=pd.read_html(url_site)
print('start')
#print(url_site)
soup = bs(r.content,"lxml")
#soup=soup.prettify()
inmates_info={}
#### fix for dif webs
for i,table in enumerate(soup.findChildren("table")):
    if i==0:
        continue
    #print(table)
    for row in table.findChildren('tr'):
        for j,col in enumerate(row.findChildren('td')):
            if col['class'][0]=='tblheading':
                continue
            if col['class'][0]=='INmateRow' and j==1:
                more_info=col.find_all('a')[0]['href'].split('"')[1]
                im_id=col.find_all('a')[0]['href'].split('"')[3]
                ims=pd.read_html(inmate_dets+more_info)
                del ims[0]
                inmate_url[im_id]=inmate_dets+more_info
                inmate_time[im_id]=str(datetime.now())#.replace(" ","_")
                inmates_info[im_id]=ims
                #rm=requests.get(inmate_dets+more_info)
                #inmate  = bs(rm.content,"lxml")
                #sys.exit()
            #print(col['class'])
with open(r'..\..\..\cobb_'+stamp+'_'+full_time+'.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, lineterminator='\n')
    spamwriter.writerow(cor_col)
    for i in inmates:
        spamwriter.writerow([i[j] for j in cor_col])
