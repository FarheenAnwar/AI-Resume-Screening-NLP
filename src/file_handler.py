# file_handler.py

import os
import re
import csv
from datetime import datetime
import uuid

def save_uploaded_file(uploaded_file):
    upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploaded_resumes'))
    os.makedirs(upload_dir, exist_ok=True)

    # Use original filename (sanitize if needed)
    original_filename = uploaded_file.name
    filepath = os.path.join(upload_dir, original_filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    # Extract text
    from resume_processing import extract_text
    text = extract_text(filepath)

    return filepath, original_filename, text

def save_candidate_info_to_csv(info_list, jd_title, preview_folder):
    output_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'candidates.csv'))
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Serial No.", "Date of Parsing", "Name", "Phone", "Email", "Experience", "Score", "Filename", "JD Title"])
        for i, info in enumerate(info_list, start=1):
            writer.writerow([
                i,
                info.get("date", ""),
                info.get("name", ""),
                info.get("phone", ""),
                info.get("email", ""),
                info.get("experience", ""),
                info.get("score", ""),
                info.get("filename", ""),
                info.get("jd_title", "")
            ])
