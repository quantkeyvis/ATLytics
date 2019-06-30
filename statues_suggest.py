# -*- coding: utf-8 -*-
# Script Exploring possible service of analyzing statue co-occurence
import numpy as np
import pandas as pd
import nltk
#import textmining as tm
from sklearn.feature_extraction.text import CountVectorizer
#import Dcluster as dcl
#import urllib
import sys
import re
import random
import glob
import pickle
import apriori

#Clean Text

charges=pd.read_csv("unodc_Charges.csv")
corpus=charges.apply(lambda s: s['Legislation / Statute / Code'] if type(s['Legislation / Statute / Code'])==type(str(' ')) else s['Statute'], axis=1)
#print(corpus.apply(lambda s: (str(type(s)),s)))
corpus=corpus.apply(lambda s: s if type(s)==type(str(' ')) else 'blank')
corpus=corpus.apply(lambda s: re.sub(';',r'\n',str(s)))
corpus=corpus.apply(lambda s: s.replace('u.s.c.s.','usc'))
corpus=corpus.apply(lambda s: s.replace('any person who',''))
corpus=corpus.apply(lambda s: s.replace('xxx',''))
corpus=corpus.apply(lambda s: s.replace('in this section',''))
corpus=corpus.apply(lambda s: s.replace('united states code section','usc'))
corpus=corpus.apply(lambda s: s.replace('criminal code','cc'))
corpus=corpus.apply(lambda s: s.replace('charge later replaced by','\n'))
corpus=corpus.apply(lambda s: s.replace('penal code','pc'))
corpus=corpus.apply(lambda s: s.replace('u.s.c.','usc'))
corpus=corpus.apply(lambda s: s.replace('u.s.c','usc'))
corpus=corpus.apply(lambda s: s.replace('the usc','usc'))
corpus=corpus.apply(lambda s: s.replace('§',''))
corpus=corpus.apply(lambda s: s.replace('united states code','usc'))
corpus=corpus.apply(lambda s: s.replace('  ',' '))
corpus=corpus.apply(lambda s: s.replace('  ',' '))
corpus=corpus.apply(lambda s: s.replace('  ',' '))
corpus=corpus.apply(lambda s: s.replace('  ',' '))
corpus=corpus.apply(lambda s: re.sub('\n',r'#',str(s).lower()))
corpus=corpus.apply(lambda s: re.sub('##',r'#',str(s)))
corpus=corpus.apply(lambda s: re.sub(r'^ ','',str(s)))
corpus=corpus.apply(lambda s: re.sub('# ',r'#',str(s)))
corpus=corpus.apply(lambda s: re.sub('# ',r'#',str(s)))
#corpus=defs['Legal Reasoning '].apply(lambda s: re.sub(r'[0-9]+',' ',str(s)))
#corpus=unodc['Summary'].apply(lambda s: str(s))
#stop_words = stopwords.words("english")


# Remove problematic symbols
stop_codec=[u'\xd2',u'\xe0',u'\u2011',u'\ude31',u'\ude0d',u'\ud83d',u'\u05d3',u'\u05de',u'\u05d7',u'\u202c',u'\xe4',u'\xf6',u'\u2013',u'\xf3',u'\xeb',u'\xad',u'\xf4'
            ,u'\u2014',u'\u0302',u'\u200b',u'\xa9',u'\xc9',u'\xed',u'\xfc',u'\xc1',u'\xd6',u'\U0001f9c0',u'\u2013',u'\xe8',u'\u20ac',u'\u2022',u'\u2026',u'\xe1'
            ,u'\xf1',u'\xfa',u'\xe7',u'\xa3',u'\xef','\xa0',u'\u2019',u'\xe9',u'\u201c',u'\u201d',u'0xc3',u'\u2018',u'\u0131',u'\u011f',u'\u015f',u'\u0159',u'\u0101'
            ,u'\u0161',u'\u0301',u'\xbf',u'\xe1',u'\ufffd',u'\u20b9',u'\xa0']

docs={}
#tdm = tm.TermDocumentMatrix()
#tdmfin=tdm(corpus)
vec = CountVectorizer(stop_words=stop_codec,token_pattern=r'^|#?([^#]+)#?|$',binary=True)
#vec = CountVectorizer(stop_words=stop_words)
X = vec.fit_transform(corpus)
X=pd.DataFrame(X.toarray(),columns=vec.get_feature_names())
#X.to_csv('Defendants_Legal_Reasoning_TDM.csv')

# Delete columns that have too long of a word or statute
for col in X.columns:
	if len(col)>90 or len(col)<4:
		#print(col)
		#print(len(col))
		#print('\n')
		del X[col]
r=X.apply(lambda s: sum(s),axis=1)
print(max(r),np.median(r),min(r))
rules=[]
poss=[]

#collect all combinations and only print combinations as a rule of thumb (rather than doing a type of binomial test) that occure more than 10% of the time
for ids, col in zip(charges['UNODC_NO'],X.columns):
	if col==' ' or col=='':
		continue
	col_cases=sum(X[col])
	col_trxns=X[X[col]>0]
	for col2 in X.columns:
		if col==col2 or col2==' ' or col2=='':
			continue
		col2_cases=sum(col_trxns[col2])
		if col2_cases>0:
			poss.append(col+' -> '+col2)
		if (col2_cases+0.0)/col_cases>0.1:
			rules.append(col+' -> '+col2+' '+str((col2_cases+0.0)/col_cases))
for el in rules:
	print(el)
print('Now possible connections\n\n')
"""for el in poss:
	print(el)"""

X['UNDOC_NO']=charges['UNODC_NO']
X.to_csv('Single_Law_Rec.csv')