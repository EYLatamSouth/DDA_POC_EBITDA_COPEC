# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# To extract text from tables in PDF
import pdfplumber
import tabula

from openai_scraper import OpenAI

# Create a function to extract text

def text_extraction(element):
    # Extracting the text from the in-line text element
    line_text = element.get_text().replace('\n', ' ')
    
    # Find the formats of the text
    # Initialize the list with all the formats that appeared in the line of text
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Iterating through each character in the line of text
            for character in text_line:
                if isinstance(character, LTChar):
                    # Append the font name of the character
                    line_formats.append(character.fontname)
                    # Append the font size of the character
                    line_formats.append(character.size)
    # Find the unique font sizes and names in the line
    format_per_line = list(set(line_formats))
    
    # Return a tuple with the text in each line along with its format
    return (line_text, format_per_line)

# Extracting tables from the page

def extract_table(pdf_path, page_num, table_num):
    # Open the pdf file
    pdf = pdfplumber.open(pdf_path)
    # Find the examined page
    table_page = pdf.pages[page_num]
    # Extract the appropriate table
    table = table_page.extract_tables()[table_num]
    return table

# Convert table into the appropriate format
def table_converter(table):
    table_string = ''
    # Iterate through each row of the table
    for row_num in range(len(table)):
        row = table[row_num]
        # Remove the line breaker from the wrapped texts
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        # Convert the table into a string 
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
    # Removing the last line break
    table_string = table_string[:-1]
    return table_string

# Find the PDF path
pdf_path = r"./Press Release 06-2023.pdf"

# Open the pdf file
pdf = pdfplumber.open(pdf_path)

# Create the dictionary to extract text from each image
text_per_page = {}

# Create an instance of the OpenAI LLM model class
llm = OpenAI()

# We extract the pages from the PDF
for pagenum, page in enumerate(extract_pages(pdf_path)):
    
    # Initialize the variables needed for the text extraction from the page
    page_text = []
    line_format = []
    page_content = []
    # Find all the elements
    page_elements = [(element.y1, element) for element in page._objs]

    # # Check the elements for tables
    # page_tables = tabula.read_pdf(pdf_path, pages=pagenum+1, multiple_tables=True) # Uncomment if java is installed for table extraction
    page_tables = []

    # Find the elements that composed a page
    for i,component in enumerate(page_elements):
        # Extract the position of the top side of the element in the PDF
        pos = component[0]
        # Extract the element of the page layout
        element = component[1]
        
        # Check if the element is a text element
        if isinstance(element, LTTextContainer):
            # Use the function to extract the text and format for each text element
            (line_text, format_per_line) = text_extraction(element)
            # Append the text of each line to the page text
            page_text.append(line_text)
            # Append the format for each line containing text
            line_format.append(format_per_line)
            page_content.append(line_text)



    # Create the key of the dictionary
    dctkey = 'Page_'+str(pagenum)
    # Add the list of list as the value of the page key
    text_per_page[dctkey]= [page_text, line_format, page_tables, page_content]
    break

# Display the content of the first page
text_to_extract = text_per_page['Page_0'][0][8]
print(text_to_extract)
# Get the response from the LLM model for the extracted text
print(llm.get_response(text_to_extract))
# Display tables from the first page
print(text_per_page['Page_0'][2])