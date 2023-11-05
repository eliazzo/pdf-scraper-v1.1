import fitz  # PyMuPDF

# Open the PDF file to extract tables
pdf_document = fitz.open('sample report card.pdf')

# Placeholder for all tables found
tables = []

# Extract tables from the the first page
page = pdf_document[0]
page_dict = page.get_text("dict", flags=fitz.TEXT_PRESERVE_IMAGES)
blocks = page_dict["blocks"]

for b in blocks:  # iterate through the text blocks
    if "lines" in b:  # if the block contains lines
        table_rows = []
        for line in b["lines"]:
            row_data = []
            for span in line["spans"]:  # Text spans within a line
                row_data.append(span["text"])
            if row_data:  # If there's data in the row, add it to the table
                table_rows.append(row_data)
        if table_rows:  # If any table-like data has been collected, add it as a table
            tables.append(table_rows)

# Close the document
pdf_document.close()

import json  # Re-import the json module for JSON operations

# Convert the table data to JSON, since we already have the 'tables' list from the previous code
json_tables = json.dumps(tables, indent=4) if tables else json.dumps("No tables found")

print (json_tables)  # print the JSON data to the console

