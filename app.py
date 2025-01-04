import streamlit as st
import functions

# Page configuration
st.set_page_config(
    page_title="ResumeAI - Smart Resume Customization",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = None
if 'job_details' not in st.session_state:
    st.session_state['job_details'] = None

# Import CSS
functions.load_css()

# Main app
def main():
    # Landing Page
    st.markdown('<h1 class="main-header">Transform Your Resume with AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get a perfectly tailored resume for every job application in seconds</p>', unsafe_allow_html=True)
    
    # Resume Tool
    tab1, tab2, tab3 = st.tabs(["Upload Resume", "Add Job Link", "Get Custom Resume"])
    
    with tab1:
        functions.upload_resume_section()
    
    with tab2:
        functions.job_link_section()
    
    with tab3:
        functions.customize_resume_section()

    # Footer
    functions.footer()

if __name__ == "__main__":
    main()
