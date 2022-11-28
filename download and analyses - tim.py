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
import pandas

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

## extract PhD position section from all files
for n in fnmatch.filter(os.listdir(folder_location), '*.txt*'):

    ## load individual file and make into a txt object
    runner_file_location = (folder_location + "/" + fnmatch.filter(os.listdir(folder_location), '*.txt*')[n])
    runner_file = open(runner_file_location, 'r')
    all_in_one_string = runner_file.read()
    
    ## find second "GradStudentPositions"
    second_GradStudentPositions_index = [i for i in range(len(all_in_one_string)) if all_in_one_string.startswith("\nGradStudentPositions", i)][1]
    ## find second "Jobs"
    second_Jobs_index = [i for i in range(len(all_in_one_string)) if all_in_one_string.startswith("\nJobs", i)][1]
    
    ## extract relevant text
    all_GradStudentPositions_string = all_in_one_string[second_GradStudentPositions_index:second_Jobs_index]

    ## no name can be after this index (problem: miss lasts position)
    end_of_PhD_names = [i for i in range(len(all_GradStudentPositions_string)) if all_GradStudentPositions_string.startswith(" . . . ", i)][-1]

    ## extract table of content
    PhD_table_of_content = all_GradStudentPositions_string[:end_of_PhD_names]
    
    ## find instances of \n to cut up PhD positions (problem: what if the position does not start with a \n)
    indices_of_PhD_start_and_end_points = [i for i in range(len(PhD_table_of_content)) if PhD_table_of_content.startswith("\n", i)][1:]
        
    ## extract PhD position names
    PhD_names = [None]*(len(indices_of_PhD_start_and_end_points)-1)
    for n in range(len(indices_of_PhD_start_and_end_points)-1):

        ## nth position
        runner = str(PhD_table_of_content[indices_of_PhD_start_and_end_points[n]:indices_of_PhD_start_and_end_points[n+1]])
        
        ## find first and last index (problem: if the PhD name is longer than the page, there are additional \ns)
        runner_first = runner.find("\\n")
        runner_last = runner.find(" .")
        
        ## extract clean name
        PhD_names[n] = runner[runner_first+2:runner_last]
    
    ## extract full PhD texts

    ## WIP
    for n in range(len(PhD_names)):

        [i for i in range(len(all_GradStudentPositions_string)) if all_GradStudentPositions_string.startswith(PhD_names[n], i)][-1]    

        runner_start = all_GradStudentPositions_string.find(PhD_names[n])
        runner_last = all_GradStudentPositions_string.find(PhD_names[n+1])

    ## bookmark









    all_GradStudentPositions_string[1:800]
    var = [i for i in range(len(all_in_one_string)) if all_in_one_string.startswith(b" .", i)]


    ## start of PhD position overview
    starter_overview_int = int(extract_first_page_raw.find("GradStudentPositions") + 21)

    ## end of PhD positions overview

    ## stop at the dots instead

    ## take the first 15 char of the first position name
    first_PhD_position = extract_first_page_raw[starter_overview_int:starter_overview_int + 15]
    ## find second instance (to identify end of the PhD overview on page 1
    ender_overview_int = int(extract_first_page_raw.find(first_PhD_position,starter_overview_int+len(first_PhD_position),))

    ## extract overview and count the numbers, to get the numbers of positions
    overview_str = extract_first_page_raw[starter_overview_int:ender_overview_int]

    ## counts all instances where a number is preceded by ". 1", ". 2", and ". 3"
    ## thus counting all positions starting on pages 10-39 (that might need adjustment?)
    total_number_positions = len([i for i in range(len(overview_str)) if overview_str.startswith(". 1", i)]) + \
                             len([i for i in range(len(overview_str)) if overview_str.startswith(". 2", i)]) + \
                             len([i for i in range(len(overview_str)) if overview_str.startswith(". 3", i)])

    ## create a list with the names of the PhD positions
    ## identify start of positions
    helper_indices = [i for i in range(len(overview_str)) if overview_str.startswith("\n", i)]

    ## create list to store names in
    PhD_names = [None] * (total_number_positions - 1)

    ## extract indices
    counter = 0
    for m in helper_indices:
        PhD_names[counter] = overview_str[m + 1: m + 15]
        counter = counter + 1

    ## remove last entry (which is empty)
    PhD_names.pop()

    ## add first PhD_position
    PhD_names.insert(0, first_PhD_position)

    ## extract PhD adverts m = PhD_names[0]
    
    PhD_start_page = [None] * (total_number_positions - 1)
    PhD_end_page = [None] * (total_number_positions - 1)
    PhD_start_position = [None] * (total_number_positions - 1)
    PhD_end_position = [None] * (total_number_positions - 1)
    
    for m in list(range(0,len(PhD_names))):

        runner_PhD_names = PhD_names[m]

        # extract text and do the search
        for i in list(range(0, writer.getNumPages())):
            pageObj = writer.getPage(i)
            text = pageObj.extractText() 
            if re.search(runner_PhD_names, text):
                PhD_start_page[m] = i
                PhD_start_position[m] = re.search(runner_PhD_names, text)
                
        
        re.search(runner_PhD_names, text)

        
        
        

    

    ## pdf_file_location = runner_file_location




## plot