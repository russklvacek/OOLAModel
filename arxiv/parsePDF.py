# importing required modules 
import PyPDF2 
import os, sys
import pandas as pd

debug = True
# creating a pdf file object 
arxivCorpus = {}

for filename in os.listdir(os.getcwd()):
    if filename[-4:] != ".pdf":
            continue

    try:
        pdfFileObj = open(filename, 'rb')
        if debug: 
            print("Opening: ", filename)

        arxivCorpus[filename] = ''
    
        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        
        # printing number of pages in pdf file 
        if debug: 
            print("Got ", pdfReader.numPages)

        for page in range(pdfReader.numPages): 
            try:
                # creating a page object 
                pageObj = pdfReader.getPage(page) 
                
                # extracting text from page 
                arxivCorpus[filename] += pageObj.extractText()
            except:
                
                if debug: 
                    e = sys.exc_info()[0]
                    print(e)
                break
        # closing the pdf file object 
        pdfFileObj.close()
    except:
        if debug:
            e = sys.exc_info()[0]
            print(e)
        pdfFileObj.close()
        continue
    
if debug:
    print(arxivCorpus)

dataset = pd.DataFrame.from_dict(arxivCorpus.items())#, orient='index')
dataset.columns = ["Paper", "Content"]
dataset.index.name = "Item"
if debug:
    print(dataset.columns)
    print(dataset)
dataset.to_json("arxivPaperData.json")
dataset.to_csv("./arxivPaperData.csv")

