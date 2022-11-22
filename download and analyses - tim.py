# packages and modules for Akhilas code
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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

    ## load individual file and make into a pdf object
    runner_file_location = str(folder_location + "/" + fnmatch.filter(os.listdir(folder_location), '*.txt*')[n])
    runner_file = open(runner_file_location, 'rb')
    runner_pdf = PyPDF2.PdfFileReader(runner_file)

    # get first page (to extract the PhD position pages from)
    first_page_raw = runner_pdf.getPage(0).extractText()

    ## identify start and end page of PhD positions from first page
    starter_PhDpage_str = first_page_raw.find("\nJobs")
    starter_PhDpage = int(first_page_raw[(starter_PhDpage_str-2):(starter_PhDpage_str)])
    ender_PhDpage_str = first_page_raw.find("\nOther")
    ender_PhDpage = int(first_page_raw[(ender_PhDpage_str-2):(ender_PhDpage_str)])

    ## extract PhD position en block from original file
    writer = PdfFileWriter()
    start = starter_PhDpage-1
    end = ender_PhDpage-1

    ## loop over all pages to extract
    while start <= end:
        ## add pages one by one
        writer.addPage(runner_pdf.getPage(start))
        ## increase counter
        start = start + 1

    ## extract number of positions in PhD position extract (which is stored in "writer")
    extract_first_page_raw = writer.getPage(0).extractText()

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