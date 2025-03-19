from PIL import Image
import openai
import pdf2image
import io
import os
import streamlit as st
import base64
from dotenv import load_dotenv
import PyPDF2
import pymongo
import bcrypt
import streamlit_authenticator as stauth

# Load environment variables
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB connection
mongo_uri = os.getenv("MONGODB_URI")
client = pymongo.MongoClient(mongo_uri)
# Replace with your database name if different
db = client["resume_analyzer_db"]
users_collection = db["users"]

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer AI",
    page_icon="📑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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

# Function to hash passwords


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify passwords


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Function to fetch users from MongoDB for streamlit-authenticator


def fetch_users():
    users = users_collection.find()
    credentials = {"usernames": {}}
    for user in users:
        credentials["usernames"][user["username"]] = {
            "name": user["username"],
            # Convert bytes to string
            "password": user["hashed_password"].decode('utf-8')
        }
    return credentials


# Initialize streamlit-authenticator
credentials = fetch_users()
authenticator = stauth.Authenticate(
    credentials,
    "resume_analyzer",  # Cookie name
    "random_key",       # Cookie key (can be any string)
    cookie_expiry_days=30
)

# Header
st.markdown(
    '<div class="header">'
    '<div class="header-icon">📑</div>'
    '<span class="header-text">Resume Analyzer AI</span>'
    '</div>',
    unsafe_allow_html=True
)

# Session state for authentication
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

# Show login/register forms only if not authenticated
if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] is False:
    mode = st.radio("Choose mode:", ("Login", "Register"))

    if mode == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = users_collection.find_one({"username": username})
            if user and verify_password(password, user["hashed_password"]):
                st.session_state["authentication_status"] = True
                st.session_state["username"] = username
                st.session_state["name"] = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Username/password is incorrect")
    elif mode == "Register":
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            elif users_collection.find_one({"username": new_username}):
                st.error("Username already exists!")
            elif new_username and new_password:
                hashed_password = hash_password(new_password)
                users_collection.insert_one(
                    {"username": new_username, "hashed_password": hashed_password})
                st.success("Registration successful! Please log in.")
                st.rerun()
            else:
                st.error("Please fill in all fields!")
else:
    # Show app content only if authenticated
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["authentication_status"] = None
        st.session_state["username"] = None
        st.session_state["name"] = None
        st.rerun()

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
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            st.image(images[0], width=200, caption="Resume Preview")
            uploaded_file.seek(0)
        except Exception:
            st.warning(
                "Unable to generate preview, but your file was uploaded.")
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
    col1, col2 = st.columns(2)
    with col1:
        analysis_btn = st.button("✓ Analyze Resume", use_container_width=True)
    with col2:
        match_btn = st.button("% Get Match Score", use_container_width=True)

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
    def extract_text_from_pdf(uploaded_file):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return "Error extracting text from PDF"

    def get_openai_response(prompt, resume_text, job_description):
        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Job Description:\n{job_description}\n\nResume Content:\n{resume_text}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error generating analysis: {e}")
            return f"Error generating analysis: {str(e)}"

    # Handle interactions
    if analysis_btn:
        if uploaded_file and input_text:
            with st.spinner("📊 Analyzing your resume against the job description..."):
                uploaded_file.seek(0)
                resume_text = extract_text_from_pdf(uploaded_file)
                response = get_openai_response(
                    input_prompt1, resume_text, input_text)
                st.markdown('<div class="results">', unsafe_allow_html=True)
                st.subheader("📋 Analysis Results")
                st.write(response)
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
                uploaded_file.seek(0)
                resume_text = extract_text_from_pdf(uploaded_file)
                response = get_openai_response(
                    input_prompt3, resume_text, input_text)
                st.markdown('<div class="results">', unsafe_allow_html=True)
                st.subheader("🎯 Match Results")
                st.write(response)
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
        <div style="margin-bottom: 10px;">Resume Analyzer AI | Made by Shubh Patel | Powered By OpenAI</div>
        <div style="font-size: 12px;">Analyze your resume against job descriptions and get AI-powered feedback</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Optional: Script to add initial users (run once, then comment out)
# """
# # Add a test user (run this once, then comment out)
# username = "testuser"
# password = "testpass123"
# hashed_password = hash_password(password)
# users_collection.insert_one({"username": username, "hashed_password": hashed_password})
# print("Test user added!")
# """
