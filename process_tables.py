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

# ==============================Convert row to a sentence==================
def row_to_sentence(row, table):
    province = row[0]
    district = row[1]
    area = row[2]
    production = row[3]
    yield_val = row[4]

    # Skip subtotal rows where district is None
    if district is None:
        return None

    sentence = (
        f"In {title}, {district} district in {province} province had "
        f"a cultivated area of {area} hectares, "
        f"production of {production} metric tonnes, "
        f"and a yield of {yield_val} Mt/Ha."
    )
    return sentence

# Test it on the first data row
test_sentence = row_to_sentence(table[1], title)
print(test_sentence)