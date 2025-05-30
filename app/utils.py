# app/utils.py
import re

def clean_text(text):
    # Remove multiple whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,;!?]', '', text)
    return text.strip()