# download
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

url = "https://evol.mcmaster.ca/cgi-bin/my_wrap/brian/evoldir/Archive/"
#folder_location = 'C:/Users/akhil/Desktop'
folder_location = 'C:/Users/timte/Documents/GitHub/Sideproject_1/downloaded'

#If there is no such folder, the script will create one automatically
if not os.path.exists(folder_location):os.mkdir(folder_location)

response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")     
for link in soup.select("a[href$='.pdf']"):
    #Name the pdf files using the last portion of each link which are unique in this case
    filename = os.path.join(folder_location,link['href'].split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(requests.get(urljoin(url,link['href'])).content)

## import pdf file
import PyPDF2

# load the pdf, make it a pdf object (don't really know what that is)
runner_pdf = open('C:/Users/timte/Downloads/Mnth_Review_Jul_22.pdf', 'rb')
runner_pdf = PyPDF2.PdfFileReader(runner_pdf)

# get first page (to extract the PhD position pages from)
first_page = runner_pdf.getPage(0)
first_page_raw = first_page.extractText()

## identify start page of PhD positions from first page
starter_PhDpage_str = first_page_raw.find("\nJobs")
starter_PhDpage = int(first_page_raw[(starter_PhDpage_str-2):(starter_PhDpage_str)])

## identify end page of PhD positions from first page
ender_PhDpage_str = first_page_raw.find("\nOther")
ender_PhDpage = int(first_page_raw[(ender_PhDpage_str-2):(ender_PhDpage_str)])

## extract pages with PhD positions
from PyPDF2 import PdfFileWriter

## use shorter variables for the loop
writer = PdfFileWriter()
start = starter_PhDpage-1
end = ender_PhDpage-1

## loop over all pages to extract
while start <= end:
    ## add pages one by one
    writer.addPage(runner_pdf.getPage(start))
    ## increase counter
    start = start + 1

## print the resulting PDF file
with open("PhD_positions.pdf", "wb") as out:
    writer.write(out)



## extract PhD positions


## look for words (gender)


## plot
