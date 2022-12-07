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

file_ID, PhD_ID, totalwordcount, word1, word2, ... wordn

output_df = pd.DataFrame(columns = ['fileID', 'PhDID', 'word1', 'word2', 'word3'],index = ['R1', 'R2', 'R3', 'R4', 'R5'])

## extract PhD position section from all files
for n in fnmatch.filter(os.listdir(folder_location), '*.txt*'):

    ## load individual file and make into a txt object
    runner_file_location = (folder_location + "/" + fnmatch.filter(os.listdir(folder_location), '*.txt*')[n])
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
    for n in range(len(indices_of_PhD_start_and_end_points)-1):

        ## nth position
        runner = str(PhD_table_of_content[indices_of_PhD_start_and_end_points[n]:indices_of_PhD_start_and_end_points[n+1]])
        
        ## find first instance of "\n"
        runner_first = runner.find("\\n")
        ## find first instance of ".."
        runner_last = runner.find("..")
        
        ## extract clean names
        PhD_names[n] = runner[runner_first+2:runner_last]
    
    ## create a version of the text without \n, as it makes searching for PhD positions impossible
    clean_all_GradStudentPositions_string = all_GradStudentPositions_string.replace("\n","")
    ## get rid of spaces as well
    clean_all_GradStudentPositions_string = clean_all_GradStudentPositions_string.replace(" ","")

    ## extract full PhD texts and look for words
    for n in range(len(PhD_names)-1):

        ## start point
        runner_first = [i for i in range(len(clean_all_GradStudentPositions_string)) if clean_all_GradStudentPositions_string.startswith(PhD_names[n], i)][1]
        ## end point
        runner_last = [i for i in range(len(clean_all_GradStudentPositions_string)) if clean_all_GradStudentPositions_string.startswith(PhD_names[n+1], i)][1]
        
        ## extract full PhD text
        runner_PhD = clean_all_GradStudentPositions_string[runner_first:runner_last]

        ## search within PhD text
        words_to_look_for = "research"
        print(len([i for i in range(len(runner_PhD)) if runner_PhD.startswith(words_to_look_for, i)]))


    ## build output row

