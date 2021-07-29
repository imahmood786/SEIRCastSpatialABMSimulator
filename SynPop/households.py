import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Utility.functions as fun
import matplotlib
import plotly.express as px
import os

def get_population(size, race):
    global races, race_dict
    result = []
    if len(races[race]) >= int(size):
        samples = races[race].sample(n=int(size))
        races[race] = races[race].drop(samples.index)
        for index, row in samples.iterrows():
            result.append(row['uid'])
        return result
    else:
        return []


#It is assumed that 85% of the total population are of same race
# https://en.wikipedia.org/wiki/Interracial_marriage_in_the_United_States

pop = pd.read_csv(os.path.join(os.getcwd(), 'SynPop', 'hillsborough_pop.csv'))
# pop = pop.head(10000)
pop = pop.sample(frac=1)

#first extract mixed sample
inter = pop.sample(frac = 0.15)
pop = pop.drop(inter.index)
races = []
#divide pop by race groups
race_groups = pop.groupby('race')
for race in race_groups:
    races.append(race[1])
races.append(inter)

race_dict = {0:'Asian', 1:'Black', 2:'Hispanic', 3:'Native', 4:'Other', 5:'Islander', 6:'Two', 7:'White', 8:'Inter'}
# houses = 800
# #https://data.census.gov/cedsci/table?q=hillsborough%20household%20size%20percent&tid=ACSST1Y2019.S2501
household_data = [['1', 28.87],
                  ['2', 33.63],
                  ['3', 16.6],
                  ['4', 12.7],
                  ['5', 5.29],
                  ['6', 1.85],
                  ['7', 1.06]]

hh_groups = [x[0] for x in household_data]
hh_probs = [x[1] for x in household_data]
hh_probs = np.array(hh_probs) / 100

hid=0
hh_df = pd.DataFrame(columns=['hid', 'size', 'occupants'])

for i,val in enumerate(races):
    print('Now processing ', race_dict[i])
    while (len(races[i])>0):
        hh_size = np.random.choice(hh_groups, size=1, p=hh_probs)[0]
        family = get_population(hh_size, i) #pass race index
        if family:
            dict = {'hid':hid, 'size': hh_size, 'occupants': family, 'race': race_dict[i]}
            hh_df = hh_df.append(dict, ignore_index = True)
            hid+=1

print(len(hh_df))
hh_df.to_csv(os.path.join(os.getcwd(), 'SynPop','hillsborough_hh.csv'), index=False)