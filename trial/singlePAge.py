from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PageObject
from PyPDF2 import Transformation
from PyPDF2 import PdfWriter, PdfReader


from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PageObject

#Open the files that have to be merged
file_path = "/Users/daminirijhwani/Downloads/checking.pdf"
pdf1File = open(file_path, 'rb')

#Read the files that you have opened
pdf1Reader = PdfFileReader(pdf1File)

#Make a list of all pages
pages = []
for pageNum in reversed(range(pdf1Reader.numPages)):
    pageObj = pdf1Reader.getPage(pageNum)
    pages.append(pageObj)

#Calculate width and height for final output page
width = pages[0].mediaBox.getWidth() + 10
height = 0
for page in pages:
    height += page.mediaBox.getHeight()

#Create blank page to merge all pages in one page
merged_page = PageObject.createBlankPage(None, width, height)

#Loop through all pages and merge / add them to blank page
y = 0
for page in pages:
    merged_page.mergeScaledTranslatedPage(page, 1, 10, y)
    y = float(y) + float(page.mediaBox.getHeight())

#Create final file with one page
writer = PdfFileWriter()
writer.addPage(merged_page)

with open('./out.pdf', 'wb') as f:
    writer.write(f)






# file_path = "/Users/daminirijhwani/Downloads/Untitled document-3.pdf"
# reader = PdfFileReader(open(file_path,'rb'))

# page_1 = reader.getPage(0)
# page_2 = reader.getPage(1)
# page_3 = reader.getPage(2)

# # total_page_height = page_1.mediaBox.getHeight() + page_2.mediaBox.getHeight() + page_3.mediaBox.getHeight()
# # print(total_page_height)
# # #Creating a new file double the size of the original
# # translated_page = PageObject.createBlankPage(None, page_1.mediaBox.getWidth(), total_page_height)
# # op = Transformation().translate(tx=page_1.mediaBox.getWidth(), ty=page_1.mediaBox.getHeight())

# #Adding the pages to the new empty page
# transformation = Transformation().translate(ty=page_2.mediaBox.getHeight()/ 2)
# page_1.add_transformation(transformation)
# page_2.merge_page(page_1, expand=True)
# # translated_page.merge_page(page_2,expand=True)
# # translated_page.merge_page(page_3,expand=True)

# writer = PdfFileWriter()
# writer.addPage(page_2)

# with open('./out.pdf', 'wb') as f:
    # writer.write(f)
