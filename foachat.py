import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure Gemini API
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Checklist based on provided requirements
checklist = [
    "The Administration shall publish on its website a FOA for each grant offered by the Administration.",
    "Each initial FOA shall include an application period of at least 30 calendar days.",
    "Each FOA shall explain each of the following when applicable:",
    "Name and purpose",
    "Duration and schedule",
    "Requirements",
    "Deadlines",
    "Anticipated funding amount at the time the FOA is published",
    "Designation as a competitive or a noncompetitive grant",
    "Evaluation criteria",
    "Method for determining a grant amount under the FOA and whether an amount other than the requested amount may be offered",
    "The required form and manner in which to submit a complete application",
    "Limitations on the offer of a grant, including the amount for an individual grant or the number of grants an applicant may receive",
    "Evaluation process",
    "Other information the Administration determines is appropriate",
    "The Administration may modify a FOA by publishing a notice of the modified provision on its website no less than 10 business days prior to the application deadline and effective date of the modified provision.",
    "The Administration shall review each complete application received using any method described in the FOA.",
    "After review of a complete application, the Administration may take any of the following actions: Offer a grant, Offer a partial grant, Hold the application for further consideration during the same fiscal year, Hold the application for further consideration in a succeeding fiscal year, Reject the application.",
    "The Administration may reject an application if: The application is not a complete application, The application is inconsistent with law, For a competitive funding opportunity, the Administration has not selected the application for a grant, The Administration determines that sufficient funding is not available, The Director of the Administration determines that offering a grant is not in the best interest of the State.",
    "The Administration shall provide written notice of the action taken within 30 days, and, if the application is rejected, the basis for the action taken.",
    "For reconsideration of an action by the Administration, the applicant shall submit a written request to the Administration within 14 business days of receiving the written notice.",
    "The written decision by the Director, or the Director’s designee, on the request for reconsideration shall be the final decision of the Administration."
]

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_document(document, reference_text):
    doc_text = extract_text_from_pdf(document) if document.type == "application/pdf" else document.getvalue().decode("utf-8")

    # Perform checklist verification
    results = []
    for item in checklist:
        if item.lower() in doc_text.lower():
            results.append((item, "Yes"))
        else:
            results.append((item, "No"))

    # Use Gemini to provide supporting evidence
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following document against the reference law and intent:

    Document to analyze:
    {doc_text}

    Reference law and intent:
    {reference_text}

    Determine if the document conforms with the intent and law from the reference. 
    Provide supporting evidence for each checklist item.
    """
    response = model.generate_content(prompt)
    supporting_evidence = response.text

    return results, supporting_evidence

def calculate_grade(results):
    total_items = len(results)
    passed_items = sum(1 for result in results if result[1] == "Yes")
    grade = (passed_items / total_items) * 100
    return grade

st.title("Document Compliance Analyzer")

# Upload reference PDF
reference_pdf = st.file_uploader("Upload reference PDF (law and intent)", type="pdf")

# Upload documents to analyze
uploaded_files = st.file_uploader("Upload documents to analyze", type=["txt", "pdf"], accept_multiple_files=True)

if reference_pdf and uploaded_files:
    reference_text = extract_text_from_pdf(reference_pdf)
    if st.button("Analyze Documents"):
        for uploaded_file in uploaded_files:
            st.write(f"Analyzing: {uploaded_file.name}")
            results, supporting_evidence = analyze_document(uploaded_file, reference_text)
            
            for item, result in results:
                st.write(f"{item}: {result}")
                st.write(f"Supporting evidence: {supporting_evidence}")
                st.divider()
            
            grade = calculate_grade(results)
            st.write(f"Final Grade: {grade:.2f}%")
            st.divider()
else:
    st.write("Please upload both a reference PDF and at least one document to analyze.")
