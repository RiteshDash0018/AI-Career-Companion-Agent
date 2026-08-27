from resume_parser.parser import extract_text_from_pdf
file_path = "data/resume.pdf"
text = extract_text_from_pdf(file_path)
print(text)