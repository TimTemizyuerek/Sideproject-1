# packages and modules for Akhilas code
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

## packages and modules for Tims code
import PyPDF2  ## handles pdf files
from PyPDF2 import PdfFileWriter ## handles pdf file
import fnmatch ## count files in directory

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

## extract PhD position section from all files
for n in fnmatch.filter(os.listdir(folder_location), '*.pdf*'):

    ## load individual file and make it a pdf object
    runner_file_location = (folder_location + "/" + fnmatch.filter(os.listdir(folder_location), '*.pdf*')[n])
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
    starter_overview_str = extract_first_page_raw.find("GradStudentPositions") + 21

    ## end of PhD positions overview
    ## take the first 14 char of the first position name
    first_PhD_position = extract_first_page_raw[starter_overview_str:starter_overview_str + 35]
    all_occurances = [i for i in range(len(extract_first_page_raw)) if extract_first_page_raw.startswith(first_PhD_position, i)]
    ender_overview_str = all_occurances[1]

    ## extract overview and count the numbers, to get the numbers of positions
    overview_str = extract_first_page_raw[starter_overview_str:ender_overview_str]

    ## counts all instances where a number is preceded by ". 1", ". 2", and ". 3"
    ## thus counting all positions starting on pages 10-39 (that might need adjustment?)
    total_number_positions = len([i for i in range(len(overview_str)) if overview_str.startswith(". 1", i)]) + \
                             len([i for i in range(len(overview_str)) if overview_str.startswith(". 2", i)]) + \
                             len([i for i in range(len(overview_str)) if overview_str.startswith(". 3", i)])



    ## your part starts here:
    ## you have the PhD positions en block in "writer"
    ## you have the number of PhD positions in "total_number_positions"

    for variable in total_number_positions:

        ## have fun :)


## plot