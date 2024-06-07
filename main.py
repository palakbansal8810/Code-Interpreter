import pdfplumber
import openpyxl
import pandas as pd
from docx import Document
import google.generativeai as genai
import json
import os 
import sys
from io import StringIO

from api import API_KEY  # Import your API_KEY from the appropriate location

# To extract text from response generated
def extract_text_from_response(response):
    try:
        candidates = response.candidates
        if candidates:
            content_parts = candidates[0].content.parts
            if content_parts:
                return content_parts[0].text
        return 'no text found in the response.'
    except Exception as e:
        return f"error: {str(e)}"


genai.configure(api_key=API_KEY)

# To generate the response
# I am using genai API to generate response because my OpenAI API limit is reached
def generate_code(file_content, user_prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([file_content, user_prompt])

    output = extract_text_from_response(response)
    return output

# to securely execute the generated Python code
def execute_code(code):
    exec_namespace = {
        '__builtins__': {} 
    }
    stdout_backup = sys.stdout
    sys.stdout = StringIO()
    try:
        exec(code, exec_namespace)
        output = sys.stdout.getvalue()
        return output
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = stdout_backup

# to read the pdf file content
def read_pdf(file_path):
    content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content += page.extract_text() + "\n"
    return content

# to read the excel file content
def read_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    return data

# to read the csv file content
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()

# to read the document file content
def read_docx(file_path):
    doc = Document(file_path)
    content = ""
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content

def response_handling(file_path, user_prompt):
    try:
        file_type = os.path.splitext(file_path)[1].lower()
        if file_type == '.pdf':
            file_content = read_pdf(file_path)
        elif file_type == '.xlsx':
            file_content = read_xlsx(file_path)
        elif file_type == '.csv':
            file_content = read_csv(file_path)
        elif file_type == '.docx':
            file_content = read_docx(file_path)
        else:
            return "Unsupported file type."

        # Generate Python code using genai API
        code = generate_code(file_content, user_prompt)
        
        
        return code
    except Exception as e:
        return str(e)

file_path = input("Enter File -\n(For eg: samples/Palak Bansal IC.pdf, samples/Admission_Predict.csv)\n\n")
user_prompt = input("Enter Prompt-\n(For eg: Tell me about this project in detail)\n\n")
result = response_handling(file_path, user_prompt)

# Print the result as needed
print(result)

