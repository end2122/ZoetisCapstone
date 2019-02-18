import multiprocessing
import re
import os
from tabula import read_pdf
from PyPDF2 import PdfFileWriter, PdfFileReader


if os.path.exists('./Data_single_pdf') == False:  # Create a Csv folder to store csv data
    os.makedirs('./Data_single_pdf')

if os.path.exists('./Csv') == False:  # Create a Csv folder to store csv data
    os.makedirs('./Csv')

#read in files' names
file_names = list()
for path, subdirs, files in os.walk(r'./Data/'):
    for filename in files:
        if filename[-4:] == '.pdf':
            file_names.append(filename)
            print(filename)


report_file_names = list()  #to store files that ar reports
data_file_names = list()  #to store files that are not reports
for file_name in file_names:
    pattern = r'Report'
    if re.search(pattern=pattern, string=file_name):
        report_file_names.append(file_name)
    else:
        data_file_names.append(file_name)


# function to convert pdf to csv
def get_csv(file_name):
    with open(f'./Data/{file_name}', 'rb') as fp: #read byte open pdf
        input_pdf = PdfFileReader(fp)  #load pdf into PyPdfReader

        file_base_name = file_name[:-4]
        if os.path.exists(f'./Data_single_pdf/{file_base_name}') == False:   #create folder for each pdf files for storing its pages
            os.makedirs(f'./Data_single_pdf/{file_base_name}')

        for i_page in range(input_pdf.numPages):  #putting each page of the pdf file into its folders
            output_pdf = PdfFileWriter()  #create Pdf
            output_pdf.addPage(input_pdf.getPage(i_page)) #loading each page into above pdf
            file_paged_name = file_base_name+str(i_page+1)
            with open(f'./Data_single_pdf/{file_base_name}/{file_paged_name}.pdf',
                      'wb') as fp:  #writing each page
                output_pdf.write(fp)

            with open(f'./Data_single_pdf/{file_base_name}/{file_paged_name}.pdf',
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
                            item.to_csv(f'./Csv/{file_paged_name}.csv')
                            print(f'success! Saveing file {file_paged_name} to csv...')
                        except:
                            print(f'Fail to convert {file_paged_name}')
                            continue
    return None

### Notice that only mac and linux allow python to use multiprocess, window GIL locks the cpu to one for python
if __name__ == '__main__':   #this part will only run as as a main, and not run when imported
    pool = multiprocessing.Pool(os.cpu_count()-1)    #use all possible cpu' thread - 1, incase the user want to do things at the samte time
    pool.map(get_csv, file_names)   #start pool.mapping the variables list to the function 
