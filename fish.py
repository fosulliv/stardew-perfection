#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd
import numpy as np
import bs4
import glob
import os
import time
import re


# In[2]:


response = requests.get('https://stardewvalleywiki.com/Stardew_Valley_Wiki').content


# In[3]:


soup = bs4.BeautifulSoup(response)
fish = bs4.BeautifulSoup(requests.get('https://stardewvalleywiki.com/Fish').content)


# In[4]:


table = fish.find('tbody')
rows1 = table.find_all('tr')


# In[27]:


def extract_fish(num, rows):
    fish_df = pd.DataFrame(columns=['Name', 'Location', 'Time', 'Season', 'Weather', 'Used In'])
    for i in range(num, len(rows), 13):
        row = rows[i]
        atts = row.find_all('td')
        name = atts[1].text.strip()
        location = atts[30].text.strip()
        time = atts[31].text.strip()
        season = atts[32].text.strip().split('\xa0')
        weather = atts[33].text.strip()
        if 37 >= len(atts):
            used_in = []
        else:
            spans = atts[37].find_all('span')
            ps = atts[37].find_all('p')
            used_in = []
            for i in spans:
                used_in.append(i.text.strip())
            for j in ps:
                used_in.append(j.text.strip().replace('\xa0', ' '))
        df_dict = {'Name': name, 'Location': location, 'Time': time, 'Season': season, 'Weather': weather, 'Used In': used_in}
        fish_df = fish_df.append(df_dict, ignore_index=True)
    return fish_df


first_fish = extract_fish(1, rows1)
rows2 = fish.find_all('table', attrs={'class': 'wikitable sortable'})[1].find_all('tr')


# In[28]:


second_fish = pd.DataFrame(columns=['Name', 'Location', 'Time', 'Season', 'Weather', 'Used In'])
for i in range(1, len(rows2), 13):
    row = rows2[i]
    atts = row.find_all('td')
    name = atts[1].text.strip()
    location = 'Night Market Submarine'
    time = '5pm - 2am'
    season = 'Winter 15th - Winter 17th'
    weather = 'Any'
    used_in = []
    df_dict = {'Name': name, 'Location': location, 'Time': time, 'Season': season, 'Weather': weather, 'Used In': used_in}
    second_fish = second_fish.append(df_dict, ignore_index=True)
    
second_fish


# In[29]:


rows3 = fish.find_all('table', attrs={'class': 'wikitable sortable'})[2].find_all('tr')
third_fish = extract_fish(1, rows3)
third_fish


# In[123]:


rows4 = fish.find_all('table', attrs={'class': 'wikitable sortable'})[4].find_all('tr')
atts = rows4[6].find_all('td')
atts[33].find_all('span')[0].text.strip()


# In[132]:


def extract_fish2(rows):
    fish_df = pd.DataFrame(columns=['Name', 'Location', 'Time', 'Season', 'Weather', 'Used In'])
    lr = len(rows)
    for i in range(lr):
        row = rows[i]
        atts = row.find_all('td')
        if len(atts) < 5:
            continue
        else:
            time = 'Any'
            season = 'All'
            weather = 'Any'
            used_in = []
            if len(atts) == 16:
                name = atts[1].text.strip()
                location = atts[12].text.strip()
                for i in atts[15].find_all('span'):
                    used_in.append(i.text.strip())
                for i in atts[15].find_all('p'):
                    used_in.append(i.text.strip().replace('\xa0', ' '))
            elif len(atts) == 34:
                name = atts[1].text.strip().strip('[3]')
                location = atts[30].text.strip()
                for i in atts[33].find_all('span'):
                    used_in.append(i.text.strip())
                for i in atts[33].find_all('p'):
                    used_in.append(i.text.strip().replace('\xa0', ' '))
                    
        dict_df = {'Name': name, 'Location': location, 'Time': time, 'Season': season, 'Weather': weather, 'Used In': used_in}
        fish_df = fish_df.append(dict_df, ignore_index=True)
    return fish_df

fourth_fish = extract_fish2(rows4)
fourth_fish


# In[147]:


all_fish = pd.concat([first_fish, second_fish, third_fish, fourth_fish], ignore_index=True)
all_fish


# In[ ]:





# In[ ]:




