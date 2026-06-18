import pdfplumber

pdf_path = "data/Statistical_Nepalese_Agriculture.pdf"
page_index = 14   # a page with a big 45-row table

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[page_index]

    # Print the page's text first, so we know what this table is ABOUT
    print("=" * 60)
    print(f"PAGE {page_index} TEXT (title/context):")
    print("=" * 60)
    text = page.extract_text() or ""
    print(text[:500])     # first 500 chars — usually has the table's title

    # Now print the extracted table, row by row
    print("\n" + "=" * 60)
    print("EXTRACTED TABLE (row by row):")
    print("=" * 60)
    tables = page.extract_tables()
    for t_index, table in enumerate(tables):
        print(f"\n--- Table {t_index} ---")
        for row in table:
            print(row)