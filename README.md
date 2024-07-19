# FOA Document Compliance Analyzer

Welcome to the FOA Document Compliance Analyzer! This tool helps you verify if your documents comply with specific legal requirements by analyzing them against a reference document. The application uses Streamlit for the user interface and Google Generative AI for advanced text analysis. The model is trained on [COMAR 14.26.02 (2024)](https://github.com/MEADecarb/FOAChat/blob/main/COMAR%2014.26.02%20%20Green%20Building%20Tax%20Credit%20Program.md)

For Additional information about MD DoIT's AI Guidance please refer to [Interim General AI Guidance](https://doit.maryland.gov/policies/Pages/InterimGenAIGuidance.aspx).
""")


[FOA Document Compliance Analyzer Application](https://foachat-dgfkxcc5krd8euggnowlkg.streamlit.app/)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Using the Application](#using-the-application)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview
The FOA Document Compliance Analyzer allows you to upload multiple documents you want to analyze. The application will check each document against a checklist of requirements and provide a detailed report with supporting evidence and a final compliance grade.

## Features
- Upload and analyze PDF and text documents.
- Verify documents against a customizable checklist.
- Generate a detailed report with supporting evidence.
- Calculate and display a final compliance grade.

## Setup Instructions
Follow these steps to set up the Document Compliance Analyzer on your local machine:

### Prerequisites
- Python 3.7 or higher
- Internet connection

### Step-by-Step Setup

#### Clone the Repository
```sh
git clone https://github.com/yourusername/document-compliance-analyzer.git
cd document-compliance-analyzer
```

#### Install Required Packages
Ensure you have pip installed. Then run:
```sh
pip install -r requirements.txt
```

#### Set Up API Key
Obtain an API key from Google Generative AI. Once you have the key, create a `secrets.toml` file in the `.streamlit` directory:
```sh
mkdir -p .streamlit
echo "[gemini]\napi_key = 'YOUR_API_KEY_HERE'" > .streamlit/secrets.toml
```

#### Run the Application
Start the Streamlit application by running:
```sh
streamlit run app.py
```
This command will open a new tab in your default web browser where you can interact with the application.

## Using the Application

### Upload Documents to Analyze
Click on the "Upload documents to analyze" button and select the documents you want to verify. You can upload multiple files at once.

### Analyze Documents
Once the documents to analyze are uploaded, click on the "Analyze Documents" button. The application will process the documents and display the results.

### View Results
For each document, the application will display:
- The checklist with "Yes" or "No" for each item.
- Supporting evidence for each checklist item.
- A final compliance grade.

## Security Considerations
Your data's security and privacy are important. Here are the cybersecurity features:

### Local Processing
All document uploads and analysis are processed locally on your machine. This means your documents are not sent to any external servers.

### API Key Protection
The Google Generative AI API key is stored in a secure `secrets.toml` file that should not be shared or exposed. Ensure this file is kept private and not included in any public repositories.

### Data Privacy
The application does not store or log any of the uploaded documents or the results of the analysis. Each session is independent, and data is cleared when the application is restarted.

## Troubleshooting

### Common Issues
- **Missing API Key**: Ensure your `secrets.toml` file is correctly configured with your Google Generative AI API key.
- **Package Installation Errors**: Ensure you have Python 3.7 or higher and pip installed. Run `pip install -r requirements.txt` to install the necessary packages.
- **Application Not Starting**: Check if Streamlit is installed by running `streamlit --version`. If not, install it using `pip install streamlit`.

### Getting Help
If you encounter any issues or have questions, please open an issue in this repository or contact us at [your-email@example.com].

## Contributing
We welcome contributions from the community! If you’d like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Open a pull request to the main repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

