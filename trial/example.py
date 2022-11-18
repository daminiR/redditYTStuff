from PyPDF2 import PdfFileReader as pr
from PyPDF2 import PdfFileWriter as pw
import os

def input_range(r):
    """
    Function to input range of numbers as list of strings and convert them into a list of int
    """
    l = []
    for num in r:
        if '-' in num:
            num = list(num.split('-'))
            num1 = int(num[0])
            num2 = int(num[1])
            for i in range(num1, num2+1):
                l.append(i-1)
        else:
            l.append(int(num)-1)

    l.sort()
    return l


def split(pdf, pages):
    """
    Function to split pdf into required pages and create a new pdf out of them, aligned sequentially
    """
    writer = pw()
    for page_num in pages:
        page = pdf.getPage(page_num)
        writer.addPage(page)

    with open("temp.pdf", 'wb') as g:
        writer.write(g)


if __name__ == "__main__":
    print("file1[r1,r2,..] file2[r1,r2,..] ... output_file_path \n   where r1 is of the form <i>(single page) or <i-j>(pages from i to j) \n Note: \t all parameters are space seperated.\n\n")
    input_data = input().split()
    output = input_data.pop(-1)
    writer = pw()
    for file in input_data:
        l1 = []
        if "[" in file and "]" in file:
            file = file.split("[")
            l1 = file[1][:-1].split(",")
            file = str(file[0])
        with open(file, 'rb') as f:
            pdf = pr(f)
            if not l1 == []:
                split(pdf=pdf, pages=input_range(l1))
                pdf = pr(open("temp.pdf", 'rb'))

            num_pages = pdf.getNumPages()
            print(num_pages)
            for page_num in range(num_pages):
                writer.addPage(pdf.getPage(page_num))
            with open(output, 'wb') as g:
                writer.write(g)
            if not l1 == []:
                os.remove("temp.pdf")
