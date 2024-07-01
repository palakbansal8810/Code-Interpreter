# Code-Interpreter

This project is a Python code interpreter that takes various file formats (PDF, XLSX, CSV, DOCX) as input, reads the content, generates Python code using the genai API, executes the generated code, and returns the result to the user.

## Installation

1. Clone the repository:
git clone https://github.com/palakbansal8810/Code-Interpreter.git 

2. Install dependencies:
pip install -r requirements.txt

3. Configure API keys:

Replace the `YOUR_API_KEY` variable in the `.env` file with your Google GenerativeAI API key.

## Usage

Run the code interpreter:

cd Code-Interpreter

python main.py

Follow the prompts to input the file path, and user prompt.
You can test the sample available in samples folder.
