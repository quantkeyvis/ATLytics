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

dat = pd.read_csv("/home/tacticalforesight/Documents/ATLytics/D4H19.csv",low_memory=False)
print(dat.columns)
for col in dat.columns:
	if 'Unnamed:' in col:
		del dat[col]
dat['noncitizen']=dat['citizenship']==dat['CountryOfExploitation']
print(dat.columns)
