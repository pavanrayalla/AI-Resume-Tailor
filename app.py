import streamlit as st
import openai
from docx import Document
import pdfkit
import os

# OpenAI API Key (Load from environment variable)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("🚀 AI Resume Tailoring Tool")

# File uploader for resume template
uploaded_file = st.file_uploader("Upload your Resume (.docx)", type=["docx"])

# Text area for job description input
job_description = st.text_area("Paste the Job Description")

# Function to generate AI suggestions
def generate_ai_suggestions(job_description, section):
    prompt = f"Generate a professional {section} section based on this job description:\n\n{job_description}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )

    return response["choices"][0]["message"]["content"].strip()

# If job description is provided, generate AI suggestions
if job_description and uploaded_file:
    st.subheader("AI-Suggested Resume Content")
    
    experience_ai = generate_ai_suggestions(job_description, "Experience")
    skills_ai = generate_ai_suggestions(job_description, "Skills")
    projects_ai = generate_ai_suggestions(job_description, "Projects")

    # Editable text areas for manual input
    experience = st.text_area("Edit Experience Section", experience_ai)
    skills = st.text_area("Edit Skills Section", skills_ai)
    projects = st.text_area("Edit Projects Section", projects_ai)

    # Function to modify the resume template
    def modify_resume(template_file, experience, skills, projects):
        doc = Document(template_file)
        
        replacements = {
            "[EXPERIENCE]": experience,
            "[SKILLS]": skills,
            "[PROJECTS]": projects
        }

        for para in doc.paragraphs:
            for key, value in replacements.items():
                if key in para.text:
                    para.text = para.text.replace(key, value)

        updated_file = "updated_resume.docx"
        doc.save(updated_file)
        return updated_file

    if st.button("Save and Download as Word"):
        with open("resume_template.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        modified_docx = modify_resume("resume_template.docx", experience, skills, projects)
        st.download_button(label="Download Updated Resume (Word)", data=open(modified_docx, "rb"), file_name="Updated_Resume.docx")

    if st.button("Save and Download as PDF"):
        pdf_file = "updated_resume.pdf"
        pdfkit.from_file("updated_resume.docx", pdf_file)
        st.download_button(label="Download Updated Resume (PDF)", data=open(pdf_file, "rb"), file_name="Updated_Resume.pdf")