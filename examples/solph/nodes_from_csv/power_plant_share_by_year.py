# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

plants = pd.read_csv('power_plants_germany.csv')
plants = plants[~np.isnan(plants.commissioned)]

fuels = ['lignite', 'coal', 'gas']
techs = ['GT', 'ST', 'CC', 'CB']#  plants.technology.unique()
flags = ['no', 'yes', np.nan]

for fuel in fuels:
    print('\n')
    for flag in flags:
        for tech in techs:

            total = plants[(plants['fuel'] == fuel)]['capacity'].sum()

            before_1970 = plants[(plants['fuel'] == fuel) &
                                 (plants['commissioned'] < 1970) &
                                 (plants['chp'] == flag) &
                                 (plants['technology'] == tech)]['capacity'].sum()

            from_1970_to_1980 = plants[(plants['fuel'] == fuel) &
                                       (plants['commissioned'] >= 1970) &
                                       (plants['commissioned'] < 1980) &
                                       (plants['chp'] == flag) &
                                       (plants['technology'] == tech)]['capacity'].sum()

            from_1980_to_1990 = plants[(plants['fuel'] == fuel) &
                                       (plants['commissioned'] >= 1980) &
                                       (plants['commissioned'] < 1990) &
                                       (plants['chp'] == flag) &
                                       (plants['technology'] == tech)]['capacity'].sum()

            from_1990_to_2000 = plants[(plants['fuel'] == fuel) &
                                       (plants['commissioned'] >= 1990) &
                                       (plants['commissioned'] < 2000) &
                                       (plants['chp'] == flag) &
                                       (plants['technology'] == tech)]['capacity'].sum()

            from_2000_to_2010 = plants[(plants['fuel'] == fuel) &
                                       (plants['commissioned'] >= 2000) &
                                       (plants['commissioned'] < 2010) &
                                       (plants['chp'] == flag) &
                                       (plants['technology'] == tech)]['capacity'].sum()

            from_2010_to_2016 = plants[(plants['fuel'] == fuel) &
                                       (plants['commissioned'] >= 2010) &
                                       (plants['commissioned'] <= 2016) &
                                       (plants['chp'] == flag) &
                                       (plants['technology'] == tech)]['capacity'].sum()

            print('## Fuel:', fuel, ' ## CHP: ', flag, ' ## TECH: ', tech)
            print(before_1970/total)
            print(from_1970_to_1980/total)
            print(from_1980_to_1990/total)
            print(from_1990_to_2000/total)
            print(from_2000_to_2010/total)
            print(from_2010_to_2016/total)

            # histogram data
            print(plants[plants['fuel'] == fuel]['commissioned'].value_counts(bins=6))


age_structure = plants[['fuel', 'commissioned']].hist(by='fuel')

eta_structure = plants[
    ~np.isnan(plants.efficiency_estimate)][
    ['fuel', 'efficiency_estimate']].hist(by='fuel')
