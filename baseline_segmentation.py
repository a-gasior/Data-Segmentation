import pandas as pd
import numpy as np
from scipy import stats

test = 'header_test.txt'
path = 'Morning/S1/Baseline/'
fname = '7'
ftype = '.txt'


df = pd.read_csv(path+fname+ftype, skiprows=[0,1,2,3,4,5,7], dtype={'Time': np.double, 'H: Right pIR': np.double}, usecols = ['Time', 'H: Right pIR'])
'''Preprocessing notes:  Remove first 6 lines of junk.  Column names are on line 6. Remove line 7--contains junk data that messes with dtype'''


df.columns = ['Time','H_Right_pIR']
'''Rename columns for easier processing. Change back to og name at end of preprocessing'''


df['exceeds'] = pd.Series((np.abs(stats.zscore(df.H_Right_pIR)) > 0.5))
'''Identify outliers(syn points) via z-test'''


peaks = []
prv = df.loc[0,'exceeds']
for idx,ele in enumerate(df.loc[1:,'exceeds']):
    if prv != ele:
        if not ele:
            peaks.append(idx)
    prv = ele
'''Separates data into its segments based on peak location''' 
    
    
segment1 = df.loc[peaks[0]:peaks[1],:]
segment2 = df.loc[peaks[1]:peaks[2],:]
s1_indexes = segment1.index
s2_indexes = segment2.index
'''Collect the indexes for the segments'''

start_to_peak_one = list(range(0,s1_indexes[0]))
peak_two_to_end = list(range(s1_indexes[-1],df.index[-1]))
seg1_inverse = start_to_peak_one
seg1_inverse.extend(peak_two_to_end)
seg1_inverse = pd.Series(seg1_inverse)
'''get the indexes of everything that is not segment1'''

start_to_peak_two = list(range(0,s2_indexes[0]))
peak_three_to_end = list(range(s2_indexes[-1],df.index[-1]))
seg2_inverse = start_to_peak_two
seg2_inverse.extend(peak_three_to_end)
seg2_inverse = pd.Series(seg2_inverse)
'''get the indexes of everything that is not segment2'''


col_names = pd.read_csv(path+fname+ftype, dtype=np.double, skiprows=[0,1,2,3,4,5,7], nrows=0)
'''get names of columns'''

del segment1,segment2,df
''' free up memory '''


col_names.to_csv('baseline_segment1.csv',index=False)
col_names.to_csv('baseline_segment2.csv',index=False)
'''Write both segment headers to file'''

chunk = 100000
for df in pd.read_csv(path+fname+ftype, skiprows=seg1_inverse, dtype=np.double, chunksize=chunk, header=None):
    df.to_csv('tout.csv', index=False, header=False, mode='a')

for df in pd.read_csv(path+fname+ftype, skiprows=seg2_inverse, dtype=np.double, chunksize=chunk, header=None):
    df.to_csv('tout.csv', index=False, header=False, mode='a')
        
