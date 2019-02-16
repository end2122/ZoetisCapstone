#!/usr/bin/env python
# coding: utf-8

# In[ ]:


path_master = r'C:/Users/endwy/Documents/Columbia MSBA/Spring 2019/E4524 - Analytics in Practice/Data/Csv/'


# In[ ]:


import pandas as pd
with open(path_master+'April 2017 - Antibiotic by Risk1.csv') as fp:
    df_ABR1 = pd.read_csv(fp,
                          skiprows=[0], 
                          usecols=['Unnamed: 1', 'Treated', 'Repulls', 'Mortalities', 'Treatment Success',
                                   'Case Fatality Rate','$/Hd/Rx', 'Treatment $'])
df_ABR1.rename(columns={'Unnamed: 1': 'Drug'}, inplace=True)
df_ABR1.head()


# In[ ]:


# Remove dashes from columns
for i in range(len(df_ABR1)):
    for j in ['Treated','Repulls','Mortalities']:
        if df_ABR1.iloc[i].loc[j] == '-':
            df_ABR1.iloc[i].loc[j] = 0
        else:
            m = df_ABR1.iloc[i].loc[j]
            m = m.replace(' ','')
            df_ABR1.iloc[i].loc[j] = m.replace(',','')
            #print(m,type(m))


# In[ ]:


# Change str -> int for numerical columns
df_ABR1['Treated'] = df_ABR1['Treated'].apply(lambda x: int(x))
df_ABR1['Repulls'] = df_ABR1['Repulls'].apply(lambda x: int(x))
df_ABR1['Mortalities'] = df_ABR1['Mortalities'].apply(lambda x: int(x))


# In[ ]:


df_ABR1.dtypes


# ### Run this below to convert to .py file before pushing to GitHub

# In[ ]:


get_ipython().system('jupyter nbconvert --to script Antibiotics_by_Risk.ipynb')

