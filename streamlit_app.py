import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Move Up: Application Tailor", page_icon="🚀")

# Hide the default Streamlit menu to make it look professional
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Instructions")
    st.write("1. Paste your **Master Resume** in the first box.")
    st.write("2. Paste the **Job Description** in the second box.")
    st.write("3. Click **Generate Application**.")
    st.info("Privacy Note: Your data is processed securely and is never saved.")

# --- MAIN PAGE ---
st.title("🚀 Job Application Tailor")
st.markdown("### Generate a keyword-optimized resume in seconds.")

# Input 1: The Master Resume
master_resume = st.text_area("Step 1: Paste your Master Resume here", height=250)

# Input 2: The Job Description
job_description = st.text_area("Step 2: Paste the Job Posting here", height=250)

# --- THE "BRAIN" (LOGIC) ---
if st.button("Generate Application", type="primary"):
    if not master_resume or not job_description:
        st.error("⚠️ Please fill in both text boxes to continue.")
    else:
        with st.spinner('Analyzing keywords and rewriting bullet points...'):
            try:
                # 1. Get the Keys from the "Safe" (Streamlit Secrets)
                api_key = st.secrets["gemini_api_key"]
                hidden_prompt = st.secrets["tailor_prompt"]

                # 2. Setup the AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                # 3. Combine Inputs with your Hidden Master Prompt
                final_prompt = f"""
                {hidden_prompt}

                ==========
                CANDIDATE MASTER RESUME:
                {master_resume}

                ==========
                TARGET JOB DESCRIPTION:
                {job_description}
                """

                # 4. Run the AI
                response = model.generate_content(final_prompt)
                
                # 5. Display the Result
                st.success("✅ Application Package Generated!")
                st.subheader("Your Custom Content")
                st.caption("Copy and paste this into your word processor.")
                st.text_area("Result:", value=response.text, height=600)

            except Exception as e:
                st.error(f"An error occurred: {e}")
