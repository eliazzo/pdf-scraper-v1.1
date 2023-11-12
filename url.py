import fitz  # PyMuPDF
import requests
import json
import os

def fetch_and_print_pdf_text_from_url(url):
    # Fetch the PDF content from the provided URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to a temporary file
        pdf_path = '/tmp/temp_pdf.pdf'  # or use any other path you prefer
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        # Now you can use the same logic as before to open and read from this file
        pdf_document = fitz.open(pdf_path)

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

        # Remove the temporary file
        os.remove(pdf_path)

        # Convert the table data to JSON, since we already have the 'tables' list from the previous code
        json_tables = json.dumps(tables, indent=4) if tables else json.dumps("No tables found")
        
        # print the JSON data to the console
        print(json_tables)
    else:
        print("Failed to fetch the PDF file from the URL.")

# Example usage:
pdf_url = 'https://example.com/sample_report_card.pdf'
fetch_and_print_pdf_text_from_url(pdf_url)
