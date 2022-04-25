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
    'hh_income_2000': 'HHINC',
    'TYPE': 'UNITTYPE',
    'NP': 'PERSONS',
}
hh_update = hh_update.rename(columns=rename_dict)

rename_dict = {
    'household_id': 'HHID',
    'AGEP': 'AGE',
    'SPORDER': 'PERID',
}
per_update = per_update.rename(columns=rename_dict)

print('writing data ...')
hh_update.to_csv('output/synthetic_households_renamed.csv', index = False)
per_update.to_csv('output/synthetic_persons_renamed.csv', index = False)
