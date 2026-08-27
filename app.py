import streamlit as st
import tempfile
import os

from dotenv import load_dotenv

from resume_parser.parser import extract_text_from_pdf
from resume_parser.extractor import extract_candidate_profile

from database.database import create_database, save_candidate


load_dotenv()

create_database()


st.set_page_config(
    page_title="AI Career Companion",
    page_icon="🎯",
    layout="wide"
)


st.title("🎯 AI Career Companion")

st.write(
    "AI-powered internship matching and interview preparation system"
)


st.header("Student Profile")


name = st.text_input("Name")

email = st.text_input("Email")

phone = st.text_input("Phone")

career_interest = st.text_input(
    "Career Interest"
)


st.header("Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


if uploaded_file:

    st.success("Resume uploaded successfully!")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_path = temp_file.name


    if st.button("Analyze Resume"):

        with st.spinner("Extracting resume information..."):

            resume_text = extract_text_from_pdf(
                temp_path
            )

            profile = extract_candidate_profile(
                resume_text
            )


        # Add manually entered information
        if name:
            profile.name = name

        if email:
            profile.email = email

        if phone:
            profile.phone = phone

        if career_interest:
            profile.career_interests = [
                career_interest
            ]


        save_candidate(profile)


        st.success(
            "Candidate profile created successfully!"
        )


        st.subheader("Candidate Information")

        st.write("**Name:**", profile.name)

        st.write("**Email:**", profile.email)

        st.write("**Phone:**", profile.phone)


        st.subheader("Skills")

        st.write(profile.skills)


        st.subheader("Education")

        for education in profile.education:

            st.write(
                f"- {education.degree} — "
                f"{education.institution} "
                f"({education.year})"
            )


        st.subheader("Experience")

        for experience in profile.experience:

            st.write(
                f"- **{experience.role}** "
                f"at {experience.company}"
            )

            st.write(
                experience.description
            )


        st.subheader("Projects")

        for project in profile.projects:

            st.write(
                f"- **{project.name}**"
            )

            st.write(
                project.description
            )


        st.subheader("Certifications")

        st.write(profile.certifications)


        os.remove(temp_path)