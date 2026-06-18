# Open and grab table and its title

import pdfplumber

pdf_path = "data/Statistical_Nepalese_Agriculture.pdf"
page_index = 14

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[page_index]
    text = page.extract_text() or ""
    tables = page.extract_tables()

# Grab the table title from the first line of the page text
title = text.split("\n")[0]
print("Title:", title)

# We'll work with the first table on the page
table = tables[0]
print("Header row:", table[0]) # table[0] is the header row. each index represents the row
print("First data row:", table[1])