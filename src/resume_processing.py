# src/resume_processing.py
import pdfplumber
import docx
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def clean_text(text):
    text = re.sub(r'\W+', ' ', text)
    text = text.lower()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

def embed(text):
    return model.encode(text).reshape(1, -1)
