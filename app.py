import streamlit as st
import PyPDF2
import docx
import requests
from datetime import datetime, timezone
import time

# Page configuration
st.set_page_config(
    page_title="ResumeAI - Smart Resume Customization",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        .main-header {
            color: #1a73e8 !important;
            font-family: 'Helvetica Neue', sans-serif !important;
            font-size: 3.5em !important;
            font-weight: 700 !important;
            text-align: center !important;
            padding: 1em 0 0.5em 0 !important;
            margin-bottom: 0.5em !important;
        }
        
        .sub-header {
            color: #5f6368 !important;
            font-family: 'Helvetica Neue', sans-serif !important;
            font-size: 1.5em !important;
            text-align: center !important;
            margin-bottom: 2em !important;
        }
        
        .feature-card {
            background-color: white !important;
            padding: 2em !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            margin: 1em !important;
            transition: transform 0.3s ease !important;
        }
        
        .feature-card:hover {
            transform: translateY(-5px) !important;
        }
        
        .stButton > button {
            background-color: #1a73e8;
            color: white;
            border-radius: 30px;
            padding: 0.5em 2em;
            border: none;
        }
        
        .stButton > button:hover {
            background-color: #1557b0;
        }
        </style>
    """, unsafe_allow_html=True)

# Helper Functions
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(docx_file):
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None

def extract_job_details(linkedin_url):
    # Mock implementation
    return {
        "title": "Sample Job Title",
        "description": "This is a sample job description with key requirements...",
        "requirements": ["Python", "Machine Learning", "Data Analysis"],
        "company": "Sample Company"
    }

def customize_resume(resume_text, job_details):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Analyzing resume...",
        "Extracting key skills...",
        "Matching with job requirements...",
        "Optimizing content...",
        "Generating final resume..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) * 20)
        time.sleep(1)
    
    return f"""
    CUSTOMIZED RESUME
    
    PROFESSIONAL SUMMARY
    Experienced professional with skills matching {job_details['title']} requirements.
    
    HIGHLIGHTED SKILLS
    {', '.join(job_details['requirements'])}
    
    [Rest of resume content would go here...]
    """

# Page Sections
def upload_resume_section():
    st.markdown("### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="We accept PDF and DOCX formats"
    )
    
    if uploaded_file:
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        st.write("File Details:", file_details)
        
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)
        
        if resume_text:
            st.session_state['resume_text'] = resume_text
            st.success("Resume uploaded successfully!")
            st.session_state['step'] = 2

def job_link_section():
    st.markdown("### 🔗 Add Job Link")
    job_url = st.text_input(
        "Paste the LinkedIn job URL",
        placeholder="https://www.linkedin.com/jobs/view/...",
        help="Enter the full LinkedIn job posting URL"
    )
    
    if job_url:
        if "linkedin.com/jobs" in job_url.lower():
            job_details = extract_job_details(job_url)
            if job_details:
                st.session_state['job_details'] = job_details
                st.success("Job details extracted successfully!")
                st.session_state['step'] = 3
        else:
            st.error("Please enter a valid LinkedIn job URL")

def customize_resume_section():
    st.markdown("### ✨ Get Your Customized Resume")
    
    if 'resume_text' not in st.session_state or 'job_details' not in st.session_state:
        st.warning("Please complete the previous steps first!")
        return
    
    if st.button("Generate Customized Resume"):
        with st.spinner("Customizing your resume..."):
            customized_resume = customize_resume(
                st.session_state['resume_text'],
                st.session_state['job_details']
            )
            
            if customized_resume:
                st.success("Resume customized successfully!")
                st.markdown("### Preview")
                st.text_area("Customized Resume", customized_resume, height=300)
                
                st.download_button(
                    label="Download Customized Resume",
                    data=customized_resume,
                    file_name="customized_resume.txt",
                    mime="text/plain"
                )

def footer():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("Version: 1.0.0")
    with col2:
        st.markdown("Last Updated: 2024-01-04")
    with col3:
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        st.markdown(f"Current Time: {current_time}")

# Main App
def main():
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state['step'] = 1
    if 'resume_text' not in st.session_state:
        st.session_state['resume_text'] = None
    if 'job_details' not in st.session_state:
        st.session_state['job_details'] = None

    # Load CSS
    load_css()

    # Landing Page
    st.markdown('<h1 class="main-header">Transform Your Resume with AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get a perfectly tailored resume for every job application in seconds</p>', unsafe_allow_html=True)
    
    # Resume Tool
    tab1, tab2, tab3 = st.tabs(["Upload Resume", "Add Job Link", "Get Custom Resume"])
    
    with tab1:
        upload_resume_section()
    
    with tab2:
        job_link_section()
    
    with tab3:
        customize_resume_section()

    # Footer
    footer()

if __name__ == "__main__":
    main()
