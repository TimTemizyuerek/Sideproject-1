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
    runner_file_location = (folder_location + "/" + fnmatch.filter(os.listdir(folder_location), '*.pdf*')[1])
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

    for m in PhD_names:






## plot