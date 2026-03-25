from pypdf import PdfReader

def read_pdf_line_by_line(pdf_path):
    """
    Reads a PDF file page by page and prints each line of text.
    
    Args:
        pdf_path (str): The path to the PDF file.
    """
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        
        # Loop through each page in the document
        tot_lines = []
        for page_num, page in enumerate(reader.pages):
            #print(f"--- Page {page_num + 1} ---")
            # Extract text from the page
            page_text = page.extract_text()
            print(page_text)
            print("****")
            # Split the text by newline characters to get individual lines
            lines = page_text.split('\n')
            tot_lines.append(lines)
        for line in tot_lines:
            index = str(line).find("My claims")
            
            if index != -1:
                line =line[:index]
               # print(line)
            
            # if "Date of service" in line:
            #     print(line)
            
# Example usage: Replace 'your_file.pdf' with your actual PDF file name
read_pdf_line_by_line('/Users/madhavathavale/Downloads/medicare_claims.pdf')
