import os
import sys
import streamlit as st
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from file_handler import save_candidate_info_to_csv, save_uploaded_file
from parser import extract_structured_info
from bias_detection import detect_sensitive_terms, debias_text
from resume_processing import extract_text, clean_text, embed
from matcher import match
from job_description import load_saved_jds, save_job_description

# --- Page Setup ---
st.set_page_config("AI Resume Matcher", layout="wide")

# --- Pastel UI Style ---
st.markdown("""
    <style>
        body {
            background-color: #22232E;
        }
        .stApp {
            background-color: #22232E;
        }
        .title-text {
            color: #44476a;
            font-weight: bold;
            font-size: 24px;
        }
        .section-header {
            color: #574b90;
            font-size: 20px;
            font-weight: 600;
        }
        .jd-box, .upload-box {
            background-color: #e3f0ff;
            padding: 15px;
            border-radius: 10px;
            color: #334155;
        }

        textarea, .stTextInput > div > input {
            background-color: #f8fbff !important;
            color: #2f3e46 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title and Description ---
st.title("AI Resume Matcher")
st.markdown("""
<div class="highlight-box">
    <h4>Upload resumes, select a job description, and instantly match candidates.</h4>
</div>
""", unsafe_allow_html=True)

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'all_infos' not in st.session_state:
    st.session_state['all_infos'] = []

# --- Admin Login ---
def admin_login():
    st.sidebar.subheader("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state['logged_in'] = True
            st.success("Logged in successfully.")
        else:
            st.error("Invalid credentials")

def admin_panel():
    st.header("Post New Job Description")
    title = st.text_input("Job Title")
    jd_text = st.text_area("Job Description")
    if st.button("Save JD"):
        if title and jd_text:
            save_job_description(title, jd_text)
            st.success("Job Description saved.")
        else:
            st.warning("Both fields are required!")

admin_login()
if st.session_state['logged_in']:
    admin_panel()

# --- Layout Columns: JD + Upload Left, Preview Right ---
st.markdown("---")
jds = load_saved_jds()
left_col, right_col = st.columns([1.2, 2])

with left_col:
    st.subheader("📄 Job Description")
    jd_options = ["--Enter manually--"] + [jd["title"] for jd in jds]
    jd_selected = st.selectbox("Choose a JD or write your own:", jd_options)

    if jd_selected == "--Enter manually--":
        job_description = st.text_area("Enter Job Description", height=200)
    else:
        job_description = next((jd['description'] for jd in jds if jd['title'] == jd_selected), "")
        st.text_area("Selected Job Description", job_description, height=200, key="selected_jd")

    if job_description:
        found_terms = detect_sensitive_terms(job_description)
        if found_terms:
            st.error(f"Potential biased terms found: {', '.join(found_terms)}")
            if st.button("Auto-Debias Job Description"):
                debiased = debias_text(job_description)
                st.text_area("Debiased Job Description", debiased, height=200, key="debiased")
                job_description = debiased
        else:
            st.success("No bias detected.")

    st.subheader("📎 Upload Resumes")
    uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Match Resumes"):
        if not job_description or not uploaded_files:
            st.warning("Please upload at least one resume and enter a job description.")
        else:
            resume_embeddings = {}
            st.session_state["all_infos"] = []

            preview_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resume_previews'))
            os.makedirs(preview_folder, exist_ok=True)

            jd_embedding = embed(clean_text(job_description))

            for uploaded_file in uploaded_files:
                saved_path, saved_name, raw_text = save_uploaded_file(uploaded_file)

                # ⛔ Debias resume before processing
                resume_terms = detect_sensitive_terms(raw_text)
                if resume_terms:
                    raw_text = debias_text(raw_text)

                cleaned = clean_text(raw_text)
                emb = embed(cleaned)

                preview_filename = saved_name.replace('.pdf', '.txt').replace('.docx', '.txt')
                resume_embeddings[preview_filename] = emb

            matched_results = match(jd_embedding, resume_embeddings)
            similarity_scores = {fname: round(score, 2) for fname, score in matched_results}

            for idx, (fname, score) in enumerate(similarity_scores.items(), start=1):
                full_path = os.path.join(preview_folder, fname)
                raw_resume_path = os.path.join(os.path.dirname(__file__), '..', 'uploaded_resumes', fname.replace('.txt', '.pdf'))
                if not os.path.exists(raw_resume_path):
                    raw_resume_path = raw_resume_path.replace('.pdf', '.docx')
                if not os.path.exists(raw_resume_path):
                    continue

                raw_text = extract_text(raw_resume_path)

                extracted = extract_structured_info(
                    raw_text,
                    score=score,
                    jd_title=jd_selected if jd_selected != "--Enter manually--" else "Manual Entry",
                    filename=fname
                )
                extracted["serial"] = idx
                st.session_state["all_infos"].append(extracted)

                # Save preview txt
                with open(full_path, "w", encoding="utf-8") as pf:
                    pf.write(f"Serial: {idx}\n")
                    pf.write(f"Name: {extracted.get('name', '')}\n")
                    pf.write(f"Email: {extracted.get('email', '')}\n")
                    pf.write(f"Phone: {extracted.get('phone', '')}\n")
                    pf.write(f"Experience: {extracted.get('experience', '')}\n")
                    pf.write(f"Upload Date: {extracted.get('upload_date', '')}\n")
                    pf.write(f"JD Title: {extracted.get('jd_title', '')}\n")
                    pf.write(f"Score: {extracted.get('score', '')}\n")
                    pf.write(f"Filename: {extracted.get('filename', '')}\n")

            jd_title = jd_selected if jd_selected != "--Enter manually--" else "Manual Entry"
            save_candidate_info_to_csv(st.session_state["all_infos"], jd_title, preview_folder)
            st.success("Candidate info saved to candidates.csv.")

with right_col:
    if st.session_state["all_infos"]:
        st.subheader("📊 Resume Previews")
        for extracted in st.session_state["all_infos"]:
            st.markdown(f"""
                <div style="
                    background-color: #f9e0e0;
                    padding: 15px;
                    border-radius: 10px;
                    color: #3e3e3e;
                    margin-bottom: 20px;
                ">
                    <h5>{extracted.get('name', 'N/A')} (Score: {extracted.get('score', '0')})</h5>
                    <p><strong>Email:</strong> {extracted.get('email', 'N/A')}</p>
                    <p><strong>Phone:</strong> {extracted.get('phone', 'N/A')}</p>
                    <p><strong>Experience:</strong> {extracted.get('experience', 'N/A')}</p>
                    <p><strong>JD Title:</strong> {extracted.get('jd_title', '')}</p>
                    <p><strong>Filename:</strong> {extracted.get('filename', '')}</p>
                </div>
            """, unsafe_allow_html=True)

