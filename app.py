import os
import streamlit as st
import io
import base64
import google.generativeai as genai 
from dotenv import load_dotenv
from PIL import Image
import PyPDF2
from streamlit_lottie import st_lottie
import json

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
st.set_page_config("AI Powered Resume Tracking System")
with open('images/welcome.json', 'r') as f:
    lottie_json = json.load(f)

# Display Lottie animation
st_lottie(lottie_json)

st.header("AI Powered Resume Tracking System")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload the resume PDF", type = ["pdf"],help="Please upload the resume in PDF format")

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

# Input prompts
input_prompt1 = """
As an experienced Technical Human Resource Manager, your expertise is invaluable in evaluating the provided resume against the specific job description.
Please share your professional insights on whether the candidate's profile aligns with the role.
Highlight both strengths and areas for improvement in the applicant's qualifications, ensuring a thorough assessment.
"""

input_prompt2 = """
In your role as a dedicated career advisor, your mission is to provide personalized suggestions for skills enhancement.
Request additional information from the user about their current skills, experiences, and career aspirations.
Based on this information, deliver constructive advice on how they can strategically enhance their skill set for continuous career development.
"""

input_prompt3 = """
Imagine yourself as an AI-powered Keyword Analyst. To identify missing keywords in the resume, 
please upload the job description or provide details about the industry and specific job requirements.
Analyze the resume to pinpoint crucial keywords that might be underrepresented in the document, ensuring a comprehensive coverage.
"""

input_prompt4 = """
As a Match Percentage Calculator, your role is crucial in determining the candidate's suitability for a job.
Please upload both the job description and the candidate's resume.
Leverage your expertise to calculate the percentage match between the required skills and the candidate's qualifications, providing a quantitative assessment.
"""

if uploaded_file is not None:
    st.write("PDF uploaded successfully")
    pdf_content = input_pdf_setup(uploaded_file)

options = ["Tell me about the resume", "How Can I Improvise my skill", "What are the keywords that are missing", "Percentage Match"]
selected_option = st.selectbox("Choose an option", options)

if st.button("Submit"):
    if uploaded_file is not None:
        if selected_option == "Tell me about the resume":
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        elif selected_option == "How Can I Improvise my skill":
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        elif selected_option == "What are the keywords that are missing":
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        elif selected_option == "Percentage Match":
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")

# Add a sidebar
st.sidebar.header('VEctorDB coming soon')

st.markdown("&#169; 2024 Lalith ")
