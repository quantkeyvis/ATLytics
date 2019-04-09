# -*- coding: utf-8 -*-

import matplotlib.image as img
from matplotlib import pyplot as plt
from pydpc import Cluster
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random
import cv2
import numpy as np
import scipy
from scipy import spatial
import sklearn 

dat = pd.read_csv("D4H19.csv",low_memory=False)
print(dat.columns)
for col in dat.columns:
	if 'Unnamed:' in col:
		del dat[col]
dat['noncitizen']=dat['citizenship']==dat['CountryOfExploitation']
dat.to_csv("D4H19_cleaned.csv")

cases = pd.read_csv("unodc_export.csv",low_memory=False)
import json
new_cols={}
new_df_len={}
print('\n\n\n')
def txt_add(s):
	return ' '.join(s)+' '
for col in 'Keywords,Procedural_Fields,Victims,Defendants,Charges'.split(','):
	cases[col]=cases[col].apply(lambda s: str(s).replace("  "," ").replace("  "," ").replace(r'\\n'," "))
	#cases[col]=cases[col].apply(lambda s: json.loads(str(s).replace("'", "\'")).keys())
	if col in 'Victims,Defendants,Charges'.split(','):
		cases[col]=cases[col].apply(lambda s: "[{'Error': 'Empty'}]" if s.lower()=='nan' else s)
		cases[col]=cases[col].apply(lambda s: eval(s))
		#print(cases[col])
		#cases[col+'_keys']=cases[col].apply(lambda s: [ ' '.join(list(eval(ls).keys())) for ls in s])
		#for ele in cases[col+'_keys'].values.tolist():
		cases[col+'_keys']=cases[col].apply(lambda s: [item for ls in s for item in ls.keys()])
		cases[col+'_cnt']=cases[col].apply(lambda s: len(s))
		new_df_len[col]=sum(cases[col+'_cnt'].values.tolist())
	else:
		cases[col]=cases[col].apply(lambda s: "{'Error': 'Empty'}" if s.lower()=='nan' else s)
		cases[col+'_keys']=cases[col].apply(lambda s: list(eval(s).keys()))
		cases[col+'_cnt']=1
	#cases[col+'_keys']=cases[col].apply(lambda s: str(s.keys()))
	new_cols[col]=[]
	print(col)
	for ele in cases[col+'_keys'].values.tolist():
		new_cols[col].extend(ele)
	new_cols[col]=list(set(new_cols[col]))
	print(new_cols[col])
	print('\n')
                                
'Victims,Defendants,Charges'
newDF={}
for col in 'Victims,Defendants,Charges'.split(','):
	newDF[col]=[]
	for row in cases.iterrows():
		#print(row)
		for i,rec in enumerate(row[1][col]):
			newDF[col].append(rec)
			newDF[col][i]['UNODC_NO']=str(row[1]['UNODC_NO'])
	pd.DataFrame(newDF[col]).to_csv("unodc_"+col+".csv")
	del cases[col]
cases.to_csv("unodc_export_cleaned.csv")
