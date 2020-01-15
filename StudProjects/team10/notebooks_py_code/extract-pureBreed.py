#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

CSV_PATH = 'C:/Users/madad/Documents/all_train_data_V8.csv'
df = pd.read_csv(CSV_PATH, header=0)

df.head(5)


# In[2]:


# create output data frame
extra_df = pd.DataFrame() 
count = 0

for i in range (0, len(df)):
    pure_breed_1 = df.iloc[i]['Breed1']
    pure_breed_2 = df.iloc[i]['Breed2']
    
    if (pure_breed_1 != pure_breed_2 
        or int(pure_breed_2) == 307 # code for mixed breed
        or int(pure_breed_1) == 307
        or pure_breed_2 == None):
        is_pure_breed = 0
    else:
        count = count + 1
        is_pure_breed = 1

    extra_df = extra_df.append({'PureBreed': is_pure_breed}, ignore_index = True)

print('Total pure breed: ', count)

assert(len(df) == len(extra_df))
df = df.join(extra_df)

df.head(5)


# In[3]:


df.to_csv('all_train_data_V8_pure_breed.csv', encoding='utf-8', index=False)


# In[ ]:




