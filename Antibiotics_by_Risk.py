#!/usr/bin/env python
# coding: utf-8

# ### Set up master path

# In[ ]:


path_master = r'C:/Users/endwy/Documents/Columbia MSBA/Spring 2019/E4524 - Analytics in Practice/Data/Csv/'


# ### ABR_1 Import

# In[ ]:


import pandas as pd
with open(path_master+'April 2017 - Antibiotic by Risk1.csv') as fp:
    df_ABR1 = pd.read_csv(fp,
                          skiprows=[0], 
                          usecols=['Unnamed: 1', 'Treated', 'Repulls', 'Mortalities', 'Treatment Success',
                                   'Case Fatality Rate','$/Hd/Rx', 'Treatment $'])
df_ABR1.rename(columns={'Unnamed: 1': 'Drug'}, inplace=True)


# ### ABR_2 Import
# ##### 11 columns, repulls split into 2 columns

# In[ ]:


import pandas as pd
with open(path_master+'April 2017 - Antibiotic by Risk2.csv') as fp:
    df_ABR2 = pd.read_csv(fp,
                         usecols=['0','1','2','3','4','5','6','8','10','11'],
                         keep_default_na=False)

df_ABR2.rename(columns={'0':'Drug', '1':'Treated', '2':'Repulls', '3':'RepullsB', '4':'Mortalities', 
                        '5':'Treatment Success', '6':'Case Fatality Rate', '8':'$/Hd/Rx',
                        '10':'Treatment $','11':'Treatment $B'}, inplace=True)
# Concatenate Treatment $ column
for i in range(len(df_ABR2)):
    df_ABR2.iloc[i].loc['Treatment $'] = (df_ABR2.iloc[i].loc['Treatment $'])+(df_ABR2.iloc[i].loc['Treatment $B'])
del df_ABR2['Treatment $B']

for i in range(len(df_ABR2)):
    df_ABR2.iloc[i].loc['Repulls'] = (df_ABR2.iloc[i].loc['Repulls'])+(df_ABR2.iloc[i].loc['RepullsB'])
del df_ABR2['RepullsB']


# ### ABR_3 Import
# ##### 10 columns, mortalities is split into 2 columns

# In[ ]:


import pandas as pd
with open(path_master+'April 2017 - Antibiotic by Risk3.csv') as fp:
    df_ABR3 = pd.read_csv(fp, 
                          usecols=['0','1','2','3','4','5','6','8','10'],
                         keep_default_na=False)
df_ABR3.rename(columns={'0':'Drug', '1':'Treated', '2':'Repulls', '3':'Mortalities', '4':'MortalitiesB', 
                        '5':'Treatment Success', '6':'Case Fatality Rate', '8':'$/Hd/Rx','10':'Treatment $'}, inplace=True)

# Concatenate mortalities column
for i in range(len(df_ABR3)):
    df_ABR3.iloc[i].loc['Mortalities'] = (df_ABR3.iloc[i].loc['Mortalities'])+(df_ABR3.iloc[i].loc['MortalitiesB'])
del df_ABR3['MortalitiesB']


# ### Fully merge all ABR versions onto df_ABR

# In[ ]:


frames = [df_ABR1, df_ABR2, df_ABR3]
df_ABR = pd.concat(frames)


# ### Function to clean fully merged df_ABR columns

# In[ ]:


def ABR_Clean(df):
    """Cleans fully merged df_ABR columns to ensure appropriate dtypes/formats"""
    # Remove dashes from columns
    for i in range(len(df)):
        for j in ['Treated','Repulls','Mortalities']:
            if df.iloc[i].loc[j] == '-':
                df.iloc[i].loc[j] = 0
            else:
                m = df.iloc[i].loc[j]
                m = m.replace(' ','')
                df.iloc[i].loc[j] = m.replace(',','')
                
    # Change str -> int for numerical columns
    df['Treated'] = df['Treated'].apply(lambda x: int(x))
    df['Repulls'] = df['Repulls'].apply(lambda x: int(x))
    df['Mortalities'] = df['Mortalities'].apply(lambda x: int(x))
    
    # Remove dollar signs from columns
    df['Treatment $'] = df['Treatment $'].apply(lambda x: x[1:])
    df['$/Hd/Rx'] = df['$/Hd/Rx'].apply(lambda x: x[1:])

    # Remove dashes from columns
    for i in range(len(df)):
        for j in ['$/Hd/Rx','Treatment $']:
            if df.iloc[i].loc[j] == '-':
                df.iloc[i].loc[j] = 0.0
            else:
                m = df.iloc[i].loc[j]
                df.iloc[i].loc[j] = m.replace(',','')
                m = m.replace(' ','')
                df.iloc[i].loc[j] = m.replace(',','')

    # Change str -> float for numerical columns
    df['Treatment $'] = df['Treatment $'].apply(lambda x: float(x))
    df['$/Hd/Rx'] = df['$/Hd/Rx'].apply(lambda x: float(x))
    
    # Remove percent signs from columns and convery str -> float
    df['Treatment Success'] = df['Treatment Success'].apply(lambda x: float(x[:-1]))
    df['Case Fatality Rate'] = df['Case Fatality Rate'].apply(lambda x: float(x[:-1]))
    
    return None


# ### Run this below to convert to .py file before pushing to GitHub

# In[ ]:


get_ipython().system('jupyter nbconvert --to script Antibiotics_by_Risk.ipynb')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### Below is the same code in the ABR_Clean function for testing purposes

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

# Change str -> int for numerical columns
df_ABR1['Treated'] = df_ABR1['Treated'].apply(lambda x: int(x))
df_ABR1['Repulls'] = df_ABR1['Repulls'].apply(lambda x: int(x))
df_ABR1['Mortalities'] = df_ABR1['Mortalities'].apply(lambda x: int(x))

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

# Remove percent signs from columns and convery str -> float
df_ABR1['Treatment Success'] = df_ABR1['Treatment Success'].apply(lambda x: float(x[:-1]))
df_ABR1['Case Fatality Rate'] = df_ABR1['Case Fatality Rate'].apply(lambda x: float(x[:-1]))

