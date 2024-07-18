import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure Gemini API
genai.configure(api_key=st.secrets["gemini"]["api_key"])

def analyze_document(document, reference_pdf):
    # Extract text from the uploaded document
    if document.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(document)
        doc_text = ""
        for page in pdf_reader.pages:
            doc_text += page.extract_text()
    else:
        doc_text = document.getvalue().decode("utf-8")

    # Extract text from the reference PDF
    pdf_reader = PyPDF2.PdfReader(reference_pdf)
    ref_text = ""
    for page in pdf_reader.pages:
        ref_text += page.extract_text()

    # Use Gemini to analyze the document
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following document against the reference law and intent:

    Document to analyze:
    {doc_text}

    Reference law and intent:
    {ref_text}

    Determine if the document conforms with the intent and law from the reference. 
    Provide a detailed analysis and explanation.
    """

    response = model.generate_content(prompt)
    return response.text

st.title("Document Compliance Analyzer")

# Upload reference PDF
reference_pdf = st.file_uploader("Upload reference PDF (law and intent)", type="pdf")

# Upload documents to analyze
uploaded_files = st.file_uploader("Upload documents to analyze", type=["txt", "pdf"], accept_multiple_files=True)

if reference_pdf and uploaded_files:
    if st.button("Analyze Documents"):
        for uploaded_file in uploaded_files:
            st.write(f"Analyzing: {uploaded_file.name}")
            analysis = analyze_document(uploaded_file, reference_pdf)
            st.write(analysis)
            st.divider()
else:
    st.write("Please upload both a reference PDF and at least one document to analyze.")
