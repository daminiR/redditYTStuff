from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PageObject
from PyPDF2 import Transformation
from PyPDF2 import PdfWriter, PdfReader

def pdfMergeSInglePage_old(rootDir):
    file_path = rootDir + "/pdf/reddit.pdf"
    pdf1File = open(file_path, 'rb')
    pdf1Reader = PdfFileReader(pdf1File)
    pages = []
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pages.append(pageObj)

    width = pages[1].mediaBox.getWidth() * 2
    height = pages[1].mediaBox.getHeight()
    merged_page = PageObject.createBlankPage(None, width, height)
    writer = PdfFileWriter()
    y =0
    merged_page = PageObject.createBlankPage(None, width, height)
    for page in range(len(pages)):
        y+=1
        if y%2!=0:
            merged_page.mergePage(pages[page])
            x=float(pages[page].mediaBox.getWidth())
            if page != len(pages) - 1:
                merged_page.mergeScaledTranslatedPage(pages[page+1], 1,x, 0)
        if y%2==0:
            writer.addPage(merged_page)
            merged_page = PageObject.createBlankPage(None, width, height)
            y=0

    out_path = rootDir + "/pdf/reddit_single_page.pdf"
    with open(out_path, 'wb') as f:
        writer.write(f)

def pdfMergeSInglePage(rootDir):
    file_path = rootDir + "/pdf/reddit.pdf"
    pdf1File = open(file_path, 'rb')
    pdf1Reader = PdfFileReader(pdf1File)
    pages = []
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pages.append(pageObj)
    width = pages[0].mediaBox.getWidth()
    height = 0
    for page in pages:
        height += page.mediaBox.getHeight()
    merged_page = PageObject.createBlankPage(None, width, height)
    y = height - pages[0].mediaBox.getHeight()
    for page in range(len(pages)):
        merged_page.mergeScaledTranslatedPage(pages[page], 1, 0, y)
        if page  != len(pages) - 1:
            y = float(y) - float(pages[page + 1].mediaBox.getHeight())
        # break
    writer = PdfFileWriter()
    writer.addPage(merged_page)
    out_path = rootDir + "/pdf/reddit_single_page.pdf"
    with open(out_path, 'wb') as f:
        writer.write(f)
