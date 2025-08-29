# AI-Resume-Screening-NLP

An AI-based application that automates the **screening of resumes against job descriptions** using **NLP and machine learning techniques**. The system extracts structured information from resumes, cleans and embeds text, and matches them with job descriptions based on semantic similarity.

---

## Project Workflow

1. **Job Description Handling**

   * Save and manage job descriptions (`job_description.py`).
   * Extract job requirements for comparison.

2. **Resume Parsing**

   * Extract text from resumes (`parser.py`, `resume_processing.py`).
   * Support for **PDF** and **DOCX** formats using `pdfplumber` and `python-docx`.

3. **Text Preprocessing**

   * Clean raw text using **regex (re)**.
   * Apply **NLTK stopwords removal** and **lemmatization**.

4. **Embedding & Feature Extraction**

   * Generate sentence embeddings using **Sentence-Transformers (all-MiniLM-L6-v2)**.

5. **Similarity Matching**

   * Compare job description and resumes using **cosine similarity** (`matcher.py`).
   * Rank resumes by highest similarity score.

6. **Bias Detection & Mitigation**

   * Detect biased words using **regex-based filtering** before evaluation.

7. **App Interface**

   * A user-friendly interface built with **Streamlit** (`app.py`).
   * Allows uploading resumes, selecting job descriptions, and viewing results with structured previews.

---

## Techniques & Tools Used

| Task                    | Libraries / Frameworks                     |
| ----------------------- | ------------------------------------------ |
| **Bias Detection**      | `re` (regex)                               |
| **File Handling**       | `os`, `csv`, `datetime`                    |
| **Resume Parsing**      | `pdfplumber`, `python-docx`                |
| **Text Cleaning**       | `nltk` (stopwords, lemmatizer)             |
| **Embedding**           | `sentence-transformers (all-MiniLM-L6-v2)` |
| **Similarity Matching** | `sklearn (cosine_similarity)`, `numpy`     |
| **Storage**             | `json`, `csv`                              |
| **App Interface**       | `streamlit`                                |

---

## Project Structure

```
.
├── app.py                # Streamlit app interface
├── matcher.py            # Resume-JD similarity matching
├── job_description.py    # Save & load job descriptions
├── parser.py             # Resume parsing & embedding
├── resume_processing.py  # Text extraction & cleaning
├── requirements.txt      # Dependencies
├── job_descriptions.json # Stored JDs
└── resume_previews/      # Structured previews of resumes
```

---

## Steps to Run the Application

1. **Clone the repository**

   ```bash
   git clone <repo-link>
   cd <repo-folder>
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the environment**

   * Windows:

     ```bash
     venv\Scripts\activate
     ```
   * Mac/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

6. **Upload resumes & job descriptions** via the interface and get ranked similarity results.

---

## Output

* **Resume Previews** (structured .txt) saved in `resume_previews/`.
* **CSV file** containing extracted structured data with similarity scores.
* **Streamlit Dashboard** for interactive use.
