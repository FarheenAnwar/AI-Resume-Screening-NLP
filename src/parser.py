# parser.py

import re
from datetime import datetime

def extract_structured_info(text, score, jd_title, filename):
    # Use the first two words of the resume text as the name
    words = text.strip().split()
    name = ' '.join(words[:2]) if len(words) >= 2 else "N/A"

    # Email extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0).strip() if email_match else "N/A"

    # Improved phone number regex (ignores years and dates)
    phone_match = re.search(
        r'(?<!\d)(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}(?!\d)',
        text
    )
    phone = phone_match.group(0).strip() if phone_match else "N/A"

    # Experience extraction (Role + (Start-End))
    experience_matches = re.findall(
        r'([A-Z][a-zA-Z\s]+?)\s*\(?(\d{4})\s*[-–to]{1,3}\s*(\d{4}|present|Present)\)?',
        text
    )
    experience = '; '.join([
        f"{role.strip()} ({start}-{end})"
        for role, start, end in experience_matches
    ]) if experience_matches else "N/A"

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "name": name,
        "email": email,
        "phone": phone,
        "experience": experience,
        "score": score,
        "filename": filename,
        "jd_title": jd_title
    }
