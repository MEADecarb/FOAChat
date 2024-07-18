import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=st.secrets["gemini"]["api_key"])

def extract_text_from_pdf(pdf_file):
  reader = PdfReader(pdf_file)
  text = ""
  for page in reader.pages:
      text += page.extract_text()
  return text

def analyze_document(document_text, reference_text):
  model = genai.GenerativeModel('gemini-pro')
  prompt = f"""
  Analyze the following document and compare it to the reference text. 
  Determine if the document conforms with the intent and law described in the reference text.
  
  Reference text:
  {reference_text}
  
  Document to analyze:
  {document_text}
  
  Provide a detailed analysis, including:
  1. Whether the document conforms with the intent of the reference text
  2. Any discrepancies or areas of non-compliance
  3. Suggestions for improvement
  """
  response = model.generate_content(prompt)
  return response.text

st.title("Document Compliance Analyzer")

# Upload reference PDF
reference_pdf = st.file_uploader("Upload reference PDF (intent and law)", type="pdf")

if reference_pdf is not None:
  reference_text = extract_text_from_pdf(reference_pdf)
  st.success("Reference PDF uploaded successfully!")

  # Upload multiple documents to analyze
  uploaded_files = st.file_uploader("Upload documents to analyze", type=["pdf", "txt"], accept_multiple_files=True)

  if uploaded_files:
      for uploaded_file in uploaded_files:
          st.write(f"Analyzing: {uploaded_file.name}")
          
          if uploaded_file.type == "application/pdf":
              document_text = extract_text_from_pdf(uploaded_file)
          else:
              document_text = uploaded_file.getvalue().decode("utf-8")
          
          analysis = analyze_document(document_text, reference_text)
          st.write(analysis)
          st.markdown("---")

else:
  st.warning("Please upload a reference PDF first.")
