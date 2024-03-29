#!/usr/bin/env python
# coding: utf-8

# ### Human Steps Before Running

# 1. Make sure to: <b>!pip install tabula-py</b>
# 2. Create a folder in your own directory called 'Data'
# 3. In the first variable, 'path_master' paste in the full link of the directory you just created

# In[1]:


# Input your own directory below
path_master = r'C:/Users/endwy/Documents/Columbia MSBA/Spring 2019/E4524 - Analytics in Practice/Data/'



import re
import os
from tabula import read_pdf
from PyPDF2 import PdfFileWriter, PdfFileReader

if os.path.exists(path_master+'Csv') == False:  # Create a Csv folder to store csv data
    os.makedirs(path_master+'Csv')

#read in files' names
file_names = list()
for path, subdirs, files in os.walk(path_master):
    for filename in files:
        file_names.append(filename)

report_file_names = list()  #to store files that ar reports
data_file_names = list()  #to store files that are not reports
for file_name in file_names:
    pattern = r'Report'
    if re.search(pattern=pattern, string=file_name):
        report_file_names.append(file_name)
    else:
        data_file_names.append(file_name)
        
for file_name in file_names:
    with open (path_master+file_name,'rb') as fp:
        input_pdf = PdfFileReader(fp)  #load pdf into PyPdfReader
        
 
        file_base_name = file_name[:-4]
        if os.path.exists(path_master+file_base_name) == False:   #create folder for each pdf files for storing its pages
            os.makedirs(path_master+file_base_name)       

        for i_page in range(input_pdf.numPages):  #putting each page of the pdf file into its folders
            output_pdf = PdfFileWriter()  #create Pdf
            output_pdf.addPage(input_pdf.getPage(i_page)) #loading each page into above pdf
            file_paged_name = file_base_name+str(i_page+1)
            
            with open(path_master+file_base_name+'/'+file_paged_name+'.pdf',
                      'wb') as fp:  #writing each page
                output_pdf.write(fp)

            with open(path_master+file_base_name+'/'+file_paged_name+'.pdf',
                      'rb') as fp:  #reading each page
                df = read_pdf(fp,
                             encodind='utf-8',
                             pages=1,
                             spreasheet=False,
                             multiple_tables=True)  #convert pdf into dataframe
                #### need to exaimine different data file to make decision on how to merge df accodingly.
                #### and then save to csv use the code below
                if isinstance(df,list):
                    for item in df:
                        try:
                            item.to_csv(path_master+'Csv/'+file_paged_name+'.csv')
                            print(f'success! Saving file {file_paged_name} to csv...')
                        except:
                            print(f'Fail to convert {file_paged_name}')
                            continue        
        


# ### Run this below to convert to .py file before pushing to GitHub

# In[ ]:


get_ipython().system('jupyter nbconvert --to script pdf_csv.ipynb')

