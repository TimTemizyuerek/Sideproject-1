# packages and modules for Akhilas code
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
## import textract come back to it during optimisation

## packages and modules for Tims code
import PyPDF2  ## handles pdf files
from PyPDF2 import PdfFileWriter ## handles pdf file
import fnmatch ## count files in directory
import re
import pandas as pd
import numpy as np

## custom functions

## converts pdf to text
def pdf_to_txt(pdf_file_location):
    
    ## read pdf file
    pdffileobj=open(pdf_file_location,'rb')
    pdfreader=PyPDF2.PdfFileReader(pdffileobj)

    ## make txt filename
    txt_name = pdf_file_location.split("/")[-1]
    txt_name = txt_name[:-3]
    txt_name = "".join(["/",txt_name, "txt"])
    ## create txt file
    runner_file = open(r"".join([folder_location, txt_name]),"a",encoding='utf-8')
    
    ## loop through the pages of the PDF
    for m in [i for i in range(pdfreader.numPages)]:
        pageobj = pdfreader.getPage(m)
        runner_page = pageobj.extractText()
        runner_file.writelines(runner_page)

## set directories and ULR
url = "https://evol.mcmaster.ca/cgi-bin/my_wrap/brian/evoldir/Archive/"
#folder_location = 'C:/Users/akhil/Desktop'
folder_location = 'C:/Users/timte/Documents/GitHub/Sideproject_1/raw downloaded files'

## download files
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
for link in soup.select("a[href$='.pdf']"):
    #Name the pdf files using the last portion of each link which are unique in this case
    filename = os.path.join(folder_location,link['href'].split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(requests.get(urljoin(url,link['href'])).content)

## ## transform files into txt
## for n in list(range(0,len(fnmatch.filter(os.listdir(folder_location), '*.pdf*')))):
## 
##     ## load individual files
##     runner_file_location = (folder_location + "/" + fnmatch.filter(os.listdir(folder_location), '*.pdf*')[n])
##     
##     ## do the transformation
##     pdf_to_txt(runner_file_location)

## create output dataframe

list_of_words = ["research","biology","letter", "application", "email", "starting"]
output_df = pd.DataFrame(columns = ['fileID', 'PhDID', *list_of_words])

## extract PhD position section from all files
for n,name in enumerate(fnmatch.filter(os.listdir(folder_location), '*.txt*')):

    ## safe file name for df later
    df_filename = fnmatch.filter(os.listdir(folder_location), '*.txt*')[n]
    
    ## load individual file and make into a txt object
    runner_file_location = (folder_location + "/" + df_filename)
    runner_file = open(runner_file_location, 'r', encoding="utf8")
    all_in_one_string = runner_file.read()
    all_in_one_string = all_in_one_string.replace(" ","")
    
    ## find second "GradStudentPositions"
    second_GradStudentPositions_index = [i for i in range(len(all_in_one_string)) if all_in_one_string.startswith("\nGradStudentPositions", i)][1]
    ## find second "Jobs"
    second_Jobs_index = [i for i in range(len(all_in_one_string)) if all_in_one_string.startswith("\nJobs", i)][1]
    
    ## extract full PhD text
    all_GradStudentPositions_string = all_in_one_string[second_GradStudentPositions_index:second_Jobs_index]
    
    ## no name can be after this index (problem: miss lasts position)
    end_of_PhD_names = [i for i in range(len(all_GradStudentPositions_string)) if all_GradStudentPositions_string.startswith(".....", i)][-1]

    ## extract table of content
    PhD_table_of_content = all_GradStudentPositions_string[:end_of_PhD_names]
    
    ## find instances of \n to cut up PhD positions (problem: what if the position does not start with a \n)
    indices_of_PhD_start_and_end_points = [i for i in range(len(PhD_table_of_content)) if PhD_table_of_content.startswith("\n", i)][1:]
    
    ## extract PhD position names
    PhD_names = [None]*(len(indices_of_PhD_start_and_end_points)-1)
    for m in range(len(indices_of_PhD_start_and_end_points)-1):

        ## nth position
        runner = str(PhD_table_of_content[indices_of_PhD_start_and_end_points[m]:indices_of_PhD_start_and_end_points[m+1]])
        
        ## find first instance of "\n"
        runner_first = runner.find("\\n")
        ## find first instance of ".."
        runner_last = runner.find("..")
        
        ## extract clean names
        PhD_names[m] = runner[runner_first+2:runner_last]
    
    ## create a version of the text without \n, as it makes searching for PhD positions impossible
    clean_all_GradStudentPositions_string = all_GradStudentPositions_string.replace("\n","")

    ## extract full PhD texts and look for words
    for k in range(len(PhD_names)-1):

        ## start point
        runner_first = [i for i in range(len(clean_all_GradStudentPositions_string)) if clean_all_GradStudentPositions_string.startswith(PhD_names[k], i)]
        ## end point
        runner_last = [i for i in range(len(clean_all_GradStudentPositions_string)) if clean_all_GradStudentPositions_string.startswith(PhD_names[k+1], i)]

        ## make watertight
        if len(runner_first) == 2 and len(runner_last) == 2:
            first_index = runner_first[1]
            last_index = runner_last[1]
        elif len(runner_first) == 2 and len(runner_last) != 2:
            first_index = runner_first[1]
            last_index = runner_last[int(np.argwhere((np.array(runner_last) - runner_first[1] >= 0) == True)[0])]  ## make it more pretty
        elif len(runner_first) != 2 and len(runner_last) == 2:
            first_index = runner_first[int(np.argwhere((np.arange(len(runner_first))%(len(runner_first)/2) == 0) == True)[1])] ## make it more pretty
            last_index = runner_last[1]
        else:
            pass
    
     ## extract full PhD text
        runner_PhD = clean_all_GradStudentPositions_string[first_index:last_index]

        ## search within PhD text
        word_count_all = [None]*(len(list_of_words))
        for i,words in enumerate(list_of_words):
            word_count_all[i] = len([i for i in range(len(runner_PhD)) if runner_PhD.startswith(words, i)])

        ## assemble row to append to the df
        runner_row = pd.Series([df_filename, PhD_names[k], *word_count_all], index=output_df.columns)
        output_df = output_df.append(runner_row, ignore_index = True)