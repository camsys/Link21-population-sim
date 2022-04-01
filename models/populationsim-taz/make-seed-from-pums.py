import numpy as np
import pandas as pd
import os

print('reading data ...')
hh = pd.read_csv('data/psam_h06.csv', dtype={'RT': 'str', 'SERIALNO': 'str'})
per = pd.read_csv('data/psam_p06.csv',dtype={'RT': 'str', 'SERIALNO': 'str', 'NAICSP': 'str'})

puma_list = [4101,
 4102,
 7701,
 7702,
 7703,
 7704,
 11300,
 6701,
 6702,
 6703,
 6704,
 6705,
 6706,
 6707,
 6708,
 6709,
 6710,
 6711,
 6712,
 4701,
 4702,
 101,
 102,
 103,
 104,
 105,
 106,
 107,
 108,
 109,
 110,
 1700,
 9901,
 9902,
 9903,
 9904,
 5301,
 5302,
 5303,
 1301,
 1302,
 1303,
 1304,
 1305,
 1306,
 1307,
 1308,
 9501,
 1309,
 9502,
 9503,
 8501,
 8502,
 8503,
 8504,
 8505,
 8506,
 8507,
 8508,
 8509,
 8510,
 8511,
 8512,
 8513,
 8514,
 7501,
 7502,
 7503,
 7504,
 7505,
 7506,
 7507,
 10100,
 5500,
 8101,
 8102,
 8103,
 8104,
 8105,
 8106,
 6101,
 6102,
 6103,
 9701,
 9702,
 9703,
 8701,
 8702]

print('making copies in memory ...')
hh_update = hh.copy()
per_update = per.copy()


# select puma within the region
hh_update = hh[hh['PUMA'].isin(puma_list)]
per_update = per_update[per_update['PUMA'].isin(puma_list)]

# exclude zero-person household
hh_update= hh_update[hh_update['NP']>0]

# exclude institutionalized group quarters 
hh_update = hh_update[hh_update['TYPE'] != 2]

# use person weight for group quarters (household weight is zero)
hh_update = pd.merge(
    left = hh_update,
    right= per_update[['SERIALNO','PWGTP']].drop_duplicates(subset=['SERIALNO']),
    how  = "left"
)

hh_update.loc[hh_update.TYPE==3, "WGTP"] = hh_update.PWGTP
hh_update.drop(columns=["PWGTP"], inplace=True)

# add household income to hh seed table
hh_update['hh_income_2018'] = 999
hh_update.loc[hh_update['ADJINC']==1080470, 'hh_income_2018'] = round((hh_update['HINCP']/1.0)*1.001264*1.07910576,2)
hh_update.loc[hh_update['ADJINC']==1073449, 'hh_income_2018'] = round((hh_update['HINCP']/1.0)*1.007588*1.06536503,2)
hh_update.loc[hh_update['ADJINC']==1054606, 'hh_income_2018'] = round((hh_update['HINCP']/1.0)*1.011189*1.04293629,2)
hh_update.loc[hh_update['ADJINC']==1031452, 'hh_income_2018'] = round((hh_update['HINCP']/1.0)*1.013097*1.01811790,2)
hh_update.loc[hh_update['ADJINC']==1010145, 'hh_income_2018'] = round((hh_update['HINCP']/1.0)*1.010145*1.00000000,2)

hh_update['hh_income_2017'] = hh_update['hh_income_2018'] * 0.97695
hh_update['hh_income_2010'] = hh_update['hh_income_2018'] * 0.87208


# add household type to hh seed table
hh_update['household_type'] = 999
hh_update.loc[hh_update['BLD'].isin([2]), 'household_type'] = 1 # single family
hh_update.loc[hh_update['BLD'].isin([4,5,6,7,8,9]), 'household_type'] = 2 # multi family
hh_update.loc[hh_update['BLD'].isin([1,10]), 'household_type'] = 3 # mobile home
hh_update.loc[hh_update['BLD'].isin([3]), 'household_type'] = 4 # duplex


# add household presence of children to hh seed table
hh_update['hh_children'] = 999
hh_update.loc[hh_update['HUPAC'].isin([4]), 'hh_children'] = 1 # no children
hh_update.loc[hh_update['HUPAC'].isin([1,2,3]), 'hh_children'] = 2 # 1 or more children


# add employment status to per seed table
per_update['employed'] = 0
per_update.loc[per_update['ESR'].isin([1,2,4,5]), 'employed'] = 1


# add standard occupation to per seed table
per_update['standard_occupation'] = '999'
per_update.loc[per_update['ESR'].isin([1,2,4,5]), 'standard_occupation'] = per_update['SOCP'].str[:2]


# add occupation to per seed table
per_update['occupation'] = 999
per_update.loc[per_update['standard_occupation'].isin(['11','13','15','17','19','27','39']), 'occupation'] = 1 # Management, Business, Science, and Arts
per_update.loc[per_update['standard_occupation'].isin(['21','23','25','29','31']), 'occupation'] = 2 # White Collar Service Occupations
per_update.loc[per_update['standard_occupation'].isin(['33','35','37']), 'occupation'] = 3 # Blue Collar Service Occupations
per_update.loc[per_update['standard_occupation'].isin(['41','43']), 'occupation'] = 4 # Sales and Office Support
per_update.loc[per_update['standard_occupation'].isin(['45','47','49']), 'occupation'] = 5 # Natural Resources, Construction, and Maintenance
per_update.loc[per_update['standard_occupation'].isin(['51','53','55']), 'occupation'] = 6 # Production, Transportation, and Material Moving


# add household workers hh seed table
hh_workers = per_update.groupby('SERIALNO')['employed'].sum().reset_index().set_index('SERIALNO')['employed'].to_dict()
hh_update['hh_workers_from_esr'] = hh_update['SERIALNO'].map(hh_workers)


# add new household number
# SERIALNO is too long to be read in popsim
hh_update.insert(0, 'hh_serial_id', value=np.arange(len(hh_update))+1)

hhnum_dict = hh_update.set_index('SERIALNO')['hh_serial_id'].to_dict()
per_update['hh_serial_id'] = per_update['SERIALNO'].map(hhnum_dict)

print('writing data ...')
hh_update.to_csv('data/seed_households.csv')
per_update.to_csv('data/seed_persons.csv')
