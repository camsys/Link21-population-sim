import numpy as np
import pandas as pd
import os

print('reading data ...')
hh_df = pd.read_csv('output/synthetic_households.csv', dtype={'PUMA': 'str'})
per_df = pd.read_csv('output/synthetic_persons.csv', dtype={'PUMA': 'str'})

print('making copies in memory ...')
hh_update = hh_df.copy()
per_update = per_df.copy()

# update variable names per model spec
rename_dict = {
    'household_id': 'HHID',
    'hh_income_2000': 'HINC',
    'TYPE': 'UNITTYPE',
    'NP': 'PERSONS',
    'hh_workers_from_esr': 'hworkers',
    'VEH': 'VEHICL',
}

hh_columns_to_keep = ['HHID', 'TAZ', 'PERSONS', 'UNITTYPE', 'HINC', 'hworkers', 'HHT', 'VEHICL']

hh_update = hh_update.rename(columns=rename_dict)
hh_update = hh_update[hh_columns_to_keep]

rename_dict = {
    'household_id': 'HHID',
    'AGEP': 'AGE',
}

per_columns_to_keep = ['HHID', 'PERID', 'OCCP', 'SOCP', 'AGE', 'SEX', 'ESR', 'pemploy', 'pstudent', 'ptype']

per_update['PERID'] = np.arange(start=1, stop=len(per_update) + 1)
per_update = per_update.rename(columns=rename_dict)
per_update = per_update[per_columns_to_keep]

print('writing data ...')
hh_update.to_csv('output/synthetic_households_renamed.csv', index = False)
per_update.to_csv('output/synthetic_persons_renamed.csv', index = False)
