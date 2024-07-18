import streamlit as st
import PyPDF2
import google.generativeai as genai
from google.api_core import retry
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def read_pdf(file):
  pdf_reader = PyPDF2.PdfReader(file)
  text = ""
  for page in pdf_reader.pages:
      text += page.extract_text()
  return text

@retry.Retry()
def analyze_document(document, reference):
  model = genai.GenerativeModel('gemini-pro')
  prompt = f"""
  Analyze the following document and compare it to the reference document. 
  Determine if the document conforms with the intent and legal requirements specified in the reference.
  
  Reference document:
  {reference}
  
  Document to analyze:
  {document}
  
  Provide a detailed analysis including:
  1. Whether the document conforms with the intent of the reference
  2. Any legal compliance issues or discrepancies
  3. Suggestions for improvement or alignment
  """
  response = model.generate_content(prompt)
  return response.text

def main():
  st.title("Document Compliance Analyzer")

  # Upload reference PDF
  st.header("Upload Reference Document")
  reference_file = st.file_uploader("Choose a reference PDF file", type="pdf")
  
  if reference_file is not None:
      reference_text = read_pdf(reference_file)
      st.success("Reference document uploaded successfully!")

      # Upload documents to analyze
      st.header("Upload Documents to Analyze")
      uploaded_files = st.file_uploader("Choose documents to analyze", type=["pdf", "txt"], accept_multiple_files=True)

      if uploaded_files:
          for uploaded_file in uploaded_files:
              st.subheader(f"Analyzing: {uploaded_file.name}")
              
              if uploaded_file.type == "application/pdf":
                  document_text = read_pdf(uploaded_file)
              else:  # Assume it's a text file
                  document_text = uploaded_file.getvalue().decode("utf-8")
              
              if st.button(f"Analyze {uploaded_file.name}"):
                  with st.spinner("Analyzing document..."):
                      analysis = analyze_document(document_text, reference_text)
                      st.write(analysis)

if __name__ == "__main__":
  main()
