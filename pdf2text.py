import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
import os
from fpdf import FPDF

## Create a function to extract text from PDF
def text_extraction(element):
    # Extracting the text from the in-line text element
    line_text = element.get_text()

    # Find the formats of the text
    # Initialize the list with all the formats that appeared in the line of text
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Iterating through each character in the line of text
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats)) # Find the unique font sizes and names in the line
    
    # Return a tuple with the text in each line along with its format
    return (line_text, format_per_line)


#Final
def required_txt(pdf_path):
    file_path = f"Material\{pdf_path}"
    # create a PDF file object
    pdfFileObj = open(file_path, 'rb')
    # create a PDF reader object
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)
    # path to output file of pdf2text
    out_file_path = f'required_{pdf_path.split(".")[0]}.txt'
    # We extract the pages from the PDF
    for pagenum, page in enumerate(extract_pages(file_path)):
        if pagenum%50 == 0: print(pagenum)
        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        line_format = []
        text_from_images = []
        page_content = []
        first_element= True
        table_extraction_flag= False
        
        # Find all the elements
        page_elements = [(element.y1, element) for element in page._objs]
        # Sort all the elements as they appear in the page 
        page_elements.sort(key=lambda a: a[0], reverse=True)
        
        # Find the elements that composed a page
        for i,component in enumerate(page_elements):
            # Extract the position of the top side of the element in the PDF
            pos= component[0]
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

        # Join each string in page_content
        result = ''.join(page_content)
        # Open the file in append mode and write the result
        with open(out_file_path, 'a', encoding='utf-8') as file:
            file.write(result.replace("/n",''))
            
    print(f"Result saved to {out_file_path}")
    
    #txt file to pdf file
    pdf = FPDF()
    with open(out_file_path, 'r',encoding = "utf-8") as f:
        # Start a new page
        pdf.add_page()
        # Set the font and font size
        pdf.set_font('Arial', size=8)
        # Read and write the text in chunks
        chunk_size = 1024*1024  # Adjust the chunk size as needed
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            pdf.write(5, chunk.encode('latin-1', 'replace').decode('latin-1'))

    # Save the PDF with the same name as the text file
    pdf_output_path = f'dummy/{out_file_path.split(".")[0]}.pdf'
    pdf.output(pdf_output_path)
    print(f"Result saved to {pdf_output_path}")
    os.remove(out_file_path)
    print("Removed",out_file_path)
    
    # Closing the pdf file object
    pdfFileObj.close()

# pdf_path = 'Silberschatz_A_databases_6th_ed.pdf'
# required_txt("trial.pdf")