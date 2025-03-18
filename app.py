from PIL import Image
import google.generativeai as genai
import pdf2image
import io
import os
import streamlit as st
import base64
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer AI",
    page_icon="📑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS directly in the app (no file import needed)
st.markdown("""
<style>
    /* Modern dark theme with vibrant accents inspired by Streamly */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #0f0c29, #1e1a45);
        color: #f0f0f0;
    }
    
    /* Glowing header effect */
    .header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 30px;
        padding: 20px;
        background: rgba(20, 18, 50, 0.7);
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(255, 63, 95, 0.3);
        border-left: 3px solid #ff3f5f;
    }
    
    .header-text {
        color: #ff3f5f;
        font-size: 32px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 63, 95, 0.5);
    }
    
    /* Card styling with sleek borders and glow effects */
    .card {
        background: rgba(20, 18, 50, 0.7);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 63, 95, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 6px 25px rgba(255, 63, 95, 0.2);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 18px;
        color: #ff3f5f;
    }
    
    /* Step indicators */
    .step {
        color: #ff3f5f;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .step:before {
        content: "";
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #ff3f5f;
        border-radius: 50%;
        margin-right: 10px;
        box-shadow: 0 0 8px #ff3f5f;
    }
    
    /* Modern buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff3f5f 0%, #ff5f8f 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        border: none;
        font-weight: 500;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(255, 63, 95, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 63, 95, 0.4);
        background: linear-gradient(135deg, #ff5f8f 0%, #ff3f5f 100%);
    }
    
    /* Input fields */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(30, 28, 70, 0.7);
        color: #f0f0f0;
        border: 1px solid rgba(255, 63, 95, 0.3);
        border-radius: 8px;
        padding: 12px;
    }
    
    /* File uploader */
    div[data-baseweb="file-uploader"] {
        background-color: rgba(30, 28, 70, 0.7);
        border: 2px dashed rgba(255, 63, 95, 0.5);
        border-radius: 10px;
        transition: all 0.3s;
    }
    
    /* Success message */
    .success-msg {
        color: #4eff91;
        padding: 12px;
        background-color: rgba(78, 255, 145, 0.1);
        border-radius: 8px;
        border-left: 3px solid #4eff91;
        display: flex;
        align-items: center;
        margin: 15px 0;
    }
    
    /* Results section */
    .results {
        background: rgba(20, 18, 50, 0.7);
        border-radius: 12px;
        padding: 25px;
        margin-top: 25px;
        border-left: 3px solid #ff3f5f;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Fixes for dark mode */
    h1, h2, h3, h4, h5, h6, p, li {
        color: #f0f0f0 !important;
    }
    
    .stSpinner > div > div > div {
        border-top-color: #ff3f5f !important;
    }
    
    /* Footer enhancements */
    .footer {
        text-align: center;
        padding: 15px;
        opacity: 0.8;
        font-size: 14px;
        color: #bbb;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 63, 95, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Modern header with icon
st.markdown(
    '<div class="header">'
    '<div class="header-icon">📑</div>'
    '<span class="header-text">Resume Analyzer AI</span>'
    '</div>',
    unsafe_allow_html=True
)

# App introduction
st.markdown(
    """
    <div style="background: rgba(20, 18, 50, 0.7); padding: 15px; border-radius: 8px; margin-bottom: 25px; 
    border-left: 3px solid #4e8cff;">
    Get professional feedback on your resume based on job descriptions. Our AI will analyze your resume and 
    provide insights to help you improve your job application.
    </div>
    """,
    unsafe_allow_html=True
)

# Step 1: Upload Resume
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step">Upload Your Resume</div>',
            unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your PDF resume here",
    type=["pdf"],
    help="We only support PDF format at the moment"
)

if uploaded_file is not None:
    st.markdown(
        '<div class="success-msg">Resume uploaded successfully</div>',
        unsafe_allow_html=True
    )
    try:
        # Preview thumbnail of first page
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        st.image(images[0], width=200, caption="Resume Preview")
        uploaded_file.seek(0)  # Reset file pointer after reading
    except Exception:
        st.warning("Unable to generate preview, but your file was uploaded.")
st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Enter Job Description
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step">Enter Job Description</div>',
            unsafe_allow_html=True)
input_text = st.text_area(
    "Paste the job description here",
    height=150,
    help="For best results, include the full job description with requirements and qualifications"
)
st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Choose Analysis Type
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step">Choose Analysis Type</div>',
            unsafe_allow_html=True)

# Improved button layout with icons
col1, col2 = st.columns(2)
with col1:
    analysis_btn = st.button("✓ Analyze Resume", use_container_width=True)
with col2:
    match_btn = st.button("% Get Match Score", use_container_width=True)

# Adding simple help text
st.markdown(
    """
    <div style="font-size: 14px; opacity: 0.7; margin-top: 10px;">
    <strong>✓ Analyze Resume</strong>: Get detailed feedback on your resume's strengths and weaknesses<br>
    <strong>% Get Match Score</strong>: Calculate how well your resume matches the job description
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Prompt templates
input_prompt1 = """
You are an experienced Technical Human Resource Manager with 15+ years of expertise in talent acquisition.
Your task is to provide a comprehensive review of the candidate's resume against the job description. Focus on:

1. Overall match evaluation (high/medium/low fit)
2. Key strengths that make the candidate competitive
3. Notable gaps or areas for improvement
4. Specific recommendations to better align the resume with the role
5. Formatting and presentation feedback

Be constructive, specific, and actionable in your feedback.
"""

input_prompt3 = """
You are a sophisticated ATS (Applicant Tracking System) scanner with deep understanding of hiring criteria.
Provide a detailed match analysis including:

1. Overall match percentage (quantified from 0-100%)
2. Top 5 matching keywords/skills found in both resume and job description
3. Top 5 missing or underemphasized keywords/skills from the job description
4. Specific sections to improve for better ATS optimization
5. 2-3 concrete suggestions for enhancing the resume's match potential

Format the response with clear sections, bullet points for readability, and highlight critical recommendations.
"""

# Core functions


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        return [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
    raise FileNotFoundError("No file uploaded")


# Handle interactions
if analysis_btn:
    if uploaded_file and input_text:
        with st.spinner("📊 Analyzing your resume against the job description..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(
                input_prompt1, pdf_content, input_text)

            st.markdown('<div class="results">', unsafe_allow_html=True)
            st.subheader("📋 Analysis Results")
            st.write(response)

            # Download button for analysis
            st.download_button(
                label="📥 Download Analysis",
                data=response,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning(
            "⚠️ Please upload your resume and enter a job description first")

if match_btn:
    if uploaded_file and input_text:
        with st.spinner("🔍 Calculating match percentage..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(
                input_prompt3, pdf_content, input_text)

            st.markdown('<div class="results">', unsafe_allow_html=True)
            st.subheader("🎯 Match Results")
            st.write(response)

            # Download button for results
            st.download_button(
                label="📥 Download Results",
                data=response,
                file_name="resume_match_results.txt",
                mime="text/plain"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning(
            "⚠️ Please upload your resume and enter a job description first")

# Enhanced footer
st.markdown(
    """
    <div class="footer">
    <div style="margin-bottom: 10px;">Resume Analyzer AI | Made by Shubh Patel | Powered By Gemini</div>
    <div style="font-size: 12px;">Analyze your resume against job descriptions and get AI-powered feedback</div>
    </div>
    """,
    unsafe_allow_html=True
)
