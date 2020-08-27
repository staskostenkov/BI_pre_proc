#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

# data loading
countries = data = pd.read_csv('country_nationality.csv')
data = pd.read_csv('2people_wiki.csv')

# data filtering for columns
countries = countries[['Country', 'Nationality']]
countries['Nationality'] = countries['Nationality'].str.lower()
data = data[['Name', 'Article',]]

# control null-values
print('countries null', countries.isnull().any)
print('data null', data.isnull().any)

# data viewing
#data = data.drop([0])
prit(data[:3])
print(countries[:3])

# manth list
months = ['january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'augest',
        'september',
        'november',
        'december']

# month dictionary for maping
months_dict = {
    'january'  : 'Jan',
    'february' : 'Feb',
    'march'    : 'Mar',
    'april'    : 'Apr',
    'may'      : 'May',
    'june'     : 'Jun',
    'july'     : 'Jul',
    'augest'   : 'Aug',
    'september': 'Sep',
    'october'  : 'Oct',
    'november' : 'Nov',
    'december' : 'Dec'
}

# creating country dictionary for maping
nationality_dict = dict((key, value) for (key, value) in zip(list(countries['Nationality']), 
                                                             list(countries['Country'])))
# articles split to words
words_df = data['Article'].str.split()
# size control 
print(words_df.shape[0])

# new columns initialisation
data['day'] = 0
data['month'] = ''
data['year'] = 0
data['status'] = ''
data['Gender'] = ''
data['Nationality'] = ''
data['Country'] = ''


for ii in range(words_df.shape[0]):
    try:
        if 'born' in words_df.iloc[ii]:
            iin = words_df.iloc[ii].index('born')
            if words_df.iloc[ii][iin+1] == 'on':
                day = words_df.iloc[ii][iin+3]
                month = words_df.iloc[ii][iin+2]
                year = words_df.iloc[ii][iin+4]
            else:
                day = words_df.iloc[ii][iin+1]
                month = words_df.iloc[ii][iin+2]
                year = words_df.iloc[ii][iin+3]
        if 'she' in words_df.iloc[ii]:
            gender = 'Female'
        if 'he' in words_df.iloc[ii]:
            gender = 'Male'

            if (month not in months) & (day in months):
                month, day = day, month

            try:
                year = int(year)
            except ValueError:
                year = 3999

            try:
                day = int(day)
            except ValueError:
                day = 77

            if day >100:
                    year = day
                    day = 0

            # vars recording to dataframe
            if month in months:
                data['day'].iloc[ii] = day
                data['month'].iloc[ii] = month
                data['year'].iloc[ii] = year
                data['Gender'].iloc[ii] = gender
                data['status'].iloc[ii] = 'good'

            # nationality finding, distance checking
            try:
                min_index_number = 10000
                born_index_number = words_df.iloc[ii].index('born')
                for nationality in list(countries.Nationality):
                    if nationality in data['Article'].iloc[ii]:
                        if (words_df.iloc[ii].index(nationality)-born_index_number)<min_index_number:
                            min_index_number = words_df.iloc[ii].index(nationality)-born_index_number
                            my_nationality = nationality
                data['Nationality'].iloc[ii] = my_nationality
                #data['Country'].iloc[ii] = data['Nationality'].iloc[ii].map(nationality_dict)
            except ValueError:
                pass
            
            print(ii, True, iin, month, day, year)
    except IndexError:
        pass
    
data['Date'] = ''
# month maping to a short format
data['Date'] = data['month'].map(months_dict)
# data format creating
data['Date'] = data['day'].astype(str) +'-'+data['Date']+'-'+data['year'].astype(str)

# not-null data filtering
data = data[data.year>0]
# nationality maping to country
data['Country'] = data1['Nationality'].map(nationality_dict)

# data saveing to a file
data[['Name','day','month','year','Gender', 'Country', 'Date']].to_csv('out_data.csv')
print(data[:6])
