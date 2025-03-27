import streamlit as st
import requests
import google.generativeai as genai
import pdf2image
import io
import base64
import webbrowser

# Configure Gemini API
genai.configure(api_key="AIzaSyCO4lF2U3tjwv5myTkqH1LUBWaWuwuedis")

# Function to fetch LinkedIn data (dummy method, scraping isn't recommended)


def get_linkedin_info(linkedin_url):
    if "linkedin.com" not in linkedin_url:
        return "Invalid LinkedIn URL"
    # Dummy response
    return f"Extracted data from LinkedIn profile: {linkedin_url}"

# Function to fetch GitHub data using public API


def get_github_info(github_url):
    username = github_url.split("/")[-1]
    github_api_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(github_api_url)
    if response.status_code == 200:
        repos = response.json()
        repo_names = [repo["name"] for repo in repos]
        return f"GitHub Repositories: {', '.join(repo_names)}"
    return "Invalid GitHub URL or User Not Found"

# Function to process resume PDF


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read(
        ), poppler_path=r"C:\Program Files (x86)\poppler\Library\bin")
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    return None


# Streamlit UI
st.set_page_config(page_title="Resume ATS Checker", page_icon="🔍")
st.header("ProTrack.ai [ATS]")

# Job Description Input
input_text = st.text_area("Job Description: ", key="input")

# Resume Upload
uploaded_file = st.file_uploader("Upload Your Resume in PDF", type=["pdf"])
if uploaded_file:
    st.write("✅ PDF Uploaded Successfully")

# LinkedIn and GitHub Inputs
linkedin_url = st.text_input("Enter your LinkedIn profile URL")
github_url = st.text_input("Enter your GitHub profile URL")

# Buttons to open LinkedIn & GitHub
col1, col2 = st.columns(2)
with col1:
    if linkedin_url:
        st.markdown(f'<a href="{linkedin_url}" target="_blank"><button style="background-color:#0A66C2; color:white; padding:5px 10px; border:none; border-radius:5px; cursor:pointer;">🔗 Open LinkedIn</button></a>', unsafe_allow_html=True)

with col2:
    if github_url:
        st.markdown(f'<a href="{github_url}" target="_blank"><button style="background-color:#333; color:white; padding:5px 10px; border:none; border-radius:5px; cursor:pointer;">🔗 Open GitHub</button></a>', unsafe_allow_html=True)

# Buttons for Resume Analysis
submit1 = st.button("📄 Analyze My Resume")
submit3 = st.button("📊 Get Percentage Match")

# Prompts
input_prompt1 = """
You are an experienced Technical HR Manager. Evaluate the resume against the job description.
Also, analyze the provided LinkedIn and GitHub data to enhance the assessment.
"""

input_prompt3 = """
You are an ATS system. Evaluate the resume and profile data to provide a match percentage.
Include missing keywords and final thoughts.
"""

# Processing
if submit1 or submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        linkedin_info = get_linkedin_info(linkedin_url)
        github_info = get_github_info(github_url)

        prompt = input_prompt1 if submit1 else input_prompt3
        response = genai.GenerativeModel('gemini-1.5-flash').generate_content([
            input_text, pdf_content[0], linkedin_info, github_info, prompt
        ]).text

        st.subheader("📝 Analysis Result")
        st.write(response)
    else:
        st.error("⚠️ Please upload a resume.")

# Footer
footer = """
<style>
.footer {position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f5f5f5;
color: #000; text-align: center; padding: 10px 0; font-size: 12px;}
</style>
<div class="footer">ProTrack created by <strong>Raginee Darade</strong></div>
"""
st.markdown(footer, unsafe_allow_html=True)
