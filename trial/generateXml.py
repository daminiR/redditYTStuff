import os
import fitz
import json

file_path = "./out.pdf"
doc = fitz.open(file_path)
page = doc.load_page(0)
tp = page.get_textpage()
blocks = tp.extractBLOCKS()
for idx, block in enumerate(blocks):
    if idx == 12:
        break
    print(block)




