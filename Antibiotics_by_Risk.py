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


# In[ ]:


# Change str -> int for numerical columns
df_ABR1['Treated'] = df_ABR1['Treated'].apply(lambda x: int(x))
df_ABR1['Repulls'] = df_ABR1['Repulls'].apply(lambda x: int(x))
df_ABR1['Mortalities'] = df_ABR1['Mortalities'].apply(lambda x: int(x))


# In[ ]:


# Remove dollar signs from columns
df_ABR1['Treatment $'] = df_ABR1['Treatment $'].apply(lambda x: x[1:])
df_ABR1['$/Hd/Rx'] = df_ABR1['$/Hd/Rx'].apply(lambda x: x[1:])

# Remove dashes from columns
for i in range(len(df_ABR1)):
    for j in ['$/Hd/Rx','Treatment $']:
        if df_ABR1.iloc[i].loc[j] == '-':
            df_ABR1.iloc[i].loc[j] = 0.0
        else:
            m = df_ABR1.iloc[i].loc[j]
            df_ABR1.iloc[i].loc[j] = m.replace(',','')
            m = m.replace(' ','')
            df_ABR1.iloc[i].loc[j] = m.replace(',','')

# Change str -> float for numerical columns
df_ABR1['Treatment $'] = df_ABR1['Treatment $'].apply(lambda x: float(x))
df_ABR1['$/Hd/Rx'] = df_ABR1['$/Hd/Rx'].apply(lambda x: float(x))


# In[ ]:


# Remove percent signs from columns and convery str -> float
df_ABR1['Treatment Success'] = df_ABR1['Treatment Success'].apply(lambda x: float(x[:-1]))
df_ABR1['Case Fatality Rate'] = df_ABR1['Case Fatality Rate'].apply(lambda x: float(x[:-1]))


# ### Run this below to convert to .py file before pushing to GitHub

# In[ ]:


get_ipython().system('jupyter nbconvert --to script Antibiotics_by_Risk.ipynb')

