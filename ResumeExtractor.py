import os
import PyPDF2
import re

def search_keywords(text, keywords):
    match_keys = []
    for keyword in keywords:
        pattern = r'\b{}(?:,)?\b'.format(keyword.lower())
        if re.search(pattern, text.lower(), re.IGNORECASE):
            match_keys.append(keyword)

    return match_keys

def extract_resumes(files_path, keywords):
    shortlisted_resumes = []
    no_match_resumes = []

    for filename in os.listdir(files_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(files_path, filename)

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                resume_text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    resume_text += page.extract_text()

                matched_keywords = search_keywords(resume_text, keywords)
                if len(matched_keywords):
                    shortlisted_resumes.append({
                        'FileName': filename,
                        'MatchKeywords': ', '.join(matched_keywords)
                    })
                else:
                    no_match_resumes.append({
                        'FileName': filename,
                        'MatchKeywords': 'No match found'
                    })

    return shortlisted_resumes, no_match_resumes
