import streamlit as st
from agents.job_matching_agent import match_candidate_to_jobs
import tempfile
import os

from dotenv import load_dotenv

from resume_parser.parser import extract_text_from_pdf
from resume_parser.extractor import extract_candidate_profile

from database.database import create_database, save_candidate

from agents.job_matching_agent import match_candidate_to_jobs


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="CareerAI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

create_database()

if "profile" not in st.session_state:
    st.session_state.profile = None

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       PAGE BACKGROUND
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(139, 92, 246, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(59, 130, 246, 0.13),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #f8f7ff 0%,
                #f1f5ff 45%,
                #edf7ff 100%
            );

        color: #1e293b;
    }


    /* ========================================================
       REMOVE SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        display: none;
    }


    /* ========================================================
       MAIN CONTENT WIDTH
       ======================================================== */

    .main .block-container {
        max-width: 1250px;

        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       TOP HEADER
       ======================================================== */

    .stApp h1 {
        color: #312e81 !important;

        font-size: 42px !important;

        font-weight: 800 !important;

        letter-spacing: -1px;
    }

    .stApp h2 {
        color: #3730a3 !important;

        font-weight: 750 !important;
    }

    .stApp h3 {
        color: #4338ca !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    .stApp p {
        color: #475569;
    }


    /* ========================================================
       CONTAINER / CARDS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background:
            rgba(255, 255, 255, 0.88);

        border: 1px solid #ddd6fe;

        border-radius: 18px;

        box-shadow:
            0 8px 25px rgba(79, 70, 229, 0.07);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {

        box-shadow:
            0 12px 30px rgba(79, 70, 229, 0.12);
    }


    /* ========================================================
       INPUT BOXES
       ======================================================== */

    div[data-baseweb="input"] {

        background-color: white;

        border: 1px solid #c7d2fe;

        border-radius: 11px;
    }

    div[data-baseweb="input"]:focus-within {

        border-color: #6366f1;

        box-shadow:
            0 0 0 2px rgba(99, 102, 241, 0.12);
    }


    /* ========================================================
       INPUT LABELS
       ======================================================== */

    label {

        color: #3730a3 !important;

        font-weight: 600 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #7c3aed
            );

        color: white !important;

        border: none !important;

        border-radius: 12px;

        min-height: 48px;

        font-size: 16px;

        font-weight: 700;

        box-shadow:
            0 7px 18px rgba(79, 70, 229, 0.20);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 12px 25px rgba(79, 70, 229, 0.30);
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {

        background:
            rgba(255, 255, 255, 0.90);

        padding: 18px;

        border-radius: 16px;

        border: 2px dashed #a5b4fc;

        box-shadow:
            0 5px 18px rgba(99, 102, 241, 0.06);
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f5f3ff
            );

        padding: 18px;

        border-radius: 17px;

        border: 1px solid #ddd6fe;

        box-shadow:
            0 6px 18px rgba(79, 70, 229, 0.08);
    }

    div[data-testid="stMetricLabel"] {

        color: #6366f1 !important;

        font-weight: 650 !important;
    }

    div[data-testid="stMetricValue"] {

        color: #312e81 !important;

        font-weight: 800 !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 13px;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    div[data-testid="stExpander"] {

        background:
            rgba(255, 255, 255, 0.92);

        border: 1px solid #ddd6fe;

        border-radius: 13px;
    }


    /* ========================================================
       PROGRESS BAR
       ======================================================== */

    div[data-testid="stProgress"] > div > div {

        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #7c3aed
            );
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                #c7d2fe,
                transparent
            ) !important;

        margin: 30px 0 !important;
    }


    /* ========================================================
       CAPTION
       ======================================================== */

    .stCaption {

        color: #64748b !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "profile" not in st.session_state:

    st.session_state.profile = None


if "matches" not in st.session_state:

    st.session_state.matches = None


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title("✦ CareerAI")

st.caption(
    "Your intelligent career companion for discovering "
    "internships that match your skills and career goals."
)

st.write(
    "AI-powered resume analysis • Semantic job search • "
    "Intelligent internship matching"
)

st.divider()


# ============================================================
# STUDENT PROFILE
# ============================================================

st.header("👤 Student Profile")

st.caption(
    "Enter your basic information before analyzing your resume."
)


col1, col2, col3 = st.columns(3)


with col1:

    name = st.text_input(
        "Full Name",
        placeholder="Enter your name"
    )


with col2:

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )


with col3:

    phone = st.text_input(
        "Phone",
        placeholder="Enter your phone number"
    )


career_interest = st.text_input(
    "🎯 Career Interest",
    placeholder=(
        "Example: Machine Learning, Data Science, "
        "Web Development"
    )
)


st.divider()


# ============================================================
# RESUME ANALYSIS
# ============================================================

st.header("📑 Resume Analysis")

st.caption(
    "Upload your PDF resume and let AI automatically "
    "extract your professional information."
)


with st.container(border=True):

    st.subheader("📄 Upload Your Resume")

    st.write(
        "Supported format: PDF"
    )

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf"]
    )


# ============================================================
# ANALYZE RESUME
# ============================================================

if uploaded_file:

    st.success(
        "✓ Resume uploaded successfully!"
    )


    if st.button(
        "✦ Analyze My Resume",
        use_container_width=True
    ):

        temp_path = None


        try:

            # ------------------------------------------------
            # Create temporary PDF
            # ------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getvalue()
                )

                temp_path = temp_file.name


            # ------------------------------------------------
            # Extract resume information
            # ------------------------------------------------

            with st.spinner(
                "✦ AI is analyzing your resume..."
            ):

                resume_text = extract_text_from_pdf(
                    temp_path
                )

                profile = extract_candidate_profile(
                    resume_text
                )


            # ------------------------------------------------
            # Update manually entered information
            # ------------------------------------------------

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


            # ------------------------------------------------
            # Save profile
            # ------------------------------------------------

            st.session_state.profile = profile

            st.session_state.matches = None

            save_candidate(profile)


            st.success(
                "🎉 Your AI career profile has been created!"
            )


        except Exception as error:

            st.error(
                f"❌ Error while analyzing resume: {error}"
            )


        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                os.remove(temp_path)


st.divider()


# ============================================================
# DISPLAY PROFILE
# ============================================================

if st.session_state.profile is not None:

    profile = st.session_state.profile


    # ========================================================
    # PROFILE OVERVIEW
    # ========================================================

    st.header("📊 Profile Overview")

    st.caption(
        "Information detected from your resume."
    )


    metric1, metric2, metric3, metric4 = st.columns(4)


    with metric1:

        st.metric(
            "🧠 Skills",
            len(profile.skills)
        )


    with metric2:

        st.metric(
            "🎓 Education",
            len(profile.education)
        )


    with metric3:

        st.metric(
            "💼 Experience",
            len(profile.experience)
        )


    with metric4:

        st.metric(
            "🚀 Projects",
            len(profile.projects)
        )


    st.divider()


    # ========================================================
    # CANDIDATE INFORMATION
    # ========================================================

    st.header("👨‍🎓 Candidate Information")


    info_col1, info_col2 = st.columns(2)


    # --------------------------------------------------------
    # PERSONAL INFORMATION
    # --------------------------------------------------------

    with info_col1:

        with st.container(border=True):

            st.subheader("👤 Personal Information")

            st.write(
                f"**Name:** "
                f"{profile.name or 'Not provided'}"
            )

            st.write(
                f"**Email:** "
                f"{profile.email or 'Not provided'}"
            )

            st.write(
                f"**Phone:** "
                f"{profile.phone or 'Not provided'}"
            )
            st.session_state.profile = profile


    # --------------------------------------------------------
    # CAREER INTERESTS
    # --------------------------------------------------------

    with info_col2:

        with st.container(border=True):

            st.subheader("🎯 Career Interests")


            if profile.career_interests:

                for interest in profile.career_interests:

                    st.info(
                        f"✦ {interest}"
                    )

            else:

                st.write(
                    "No career interests detected."
                )


    # ========================================================
    # SKILLS
    # ========================================================

    st.header("🧠 Skills")

    st.caption(
        "Skills automatically identified from your resume."
    )


    with st.container(border=True):

        if profile.skills:

            skill_columns = st.columns(4)


            for index, skill in enumerate(
                profile.skills
            ):

                with skill_columns[
                    index % 4
                ]:

                    st.info(
                        f"✓ {skill}"
                    )

        else:

            st.write(
                "No skills detected."
            )


    # ========================================================
    # EDUCATION
    # ========================================================

    st.header("🎓 Education")


    if profile.education:

        education_columns = st.columns(
            min(len(profile.education), 3)
        )


        for index, education in enumerate(
            profile.education
        ):

            with education_columns[
                index % len(education_columns)
            ]:

                with st.container(border=True):

                    st.subheader(
                        f"🎓 {education.degree}"
                    )

                    st.write(
                        f"🏫 {education.institution}"
                    )

                    st.write(
                        f"📅 {education.year}"
                    )

    else:

        st.info(
            "No education information detected."
        )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    st.header("💼 Experience")


    if profile.experience:

        experience_columns = st.columns(
            min(len(profile.experience), 3)
        )


        for index, experience in enumerate(
            profile.experience
        ):

            with experience_columns[
                index % len(experience_columns)
            ]:

                with st.container(border=True):

                    st.subheader(
                        f"💼 {experience.role}"
                    )

                    st.write(
                        f"🏢 {experience.company}"
                    )

                    st.write(
                        f"⏱ {experience.duration}"
                    )

                    if experience.description:

                        st.write(
                            experience.description
                        )

    else:

        st.info(
            "No experience information detected."
        )


    # ========================================================
    # PROJECTS
    # ========================================================

    st.header("🚀 Projects")


    if profile.projects:

        project_columns = st.columns(
            min(len(profile.projects), 3)
        )


        for index, project in enumerate(
            profile.projects
        ):

            with project_columns[
                index % len(project_columns)
            ]:

                with st.container(border=True):

                    st.subheader(
                        f"✦ {project.name}"
                    )

                    st.write(
                        project.description
                    )


                    if project.technologies:

                        st.caption(
                            "Technologies used"
                        )

                        st.write(
                            ", ".join(
                                project.technologies
                            )
                        )

    else:

        st.info(
            "No projects detected."
        )


    # ========================================================
    # CERTIFICATIONS
    # ========================================================

    st.header("🏆 Certifications")


    if profile.certifications:

        with st.container(border=True):

            for certification in profile.certifications:

                st.write(
                    f"🏆 {certification}"
                )

    else:

        st.info(
            "No certifications detected."
        )


    st.divider()


    # ========================================================
    # INTERNSHIP RECOMMENDATIONS
    # ========================================================

    st.header("🎯 Internship Recommendations")

    st.caption(
        "AI-powered recommendations based on your "
        "skills, education, experience and projects."
    )


    with st.container(border=True):

        st.subheader(
            "✦ Find internships that fit your profile"
        )

        st.write(
            "Our system uses semantic search and "
            "compatibility scoring to identify relevant "
            "internship opportunities from the knowledge base."
        )


    if st.button(
        "🔎 Find My Internship Matches",
        use_container_width=True
    ):

        with st.spinner(
            "🔎 Searching the internship knowledge base..."
        ):

            try:

                matches = match_candidate_to_jobs(
                    profile,
                    top_k=5
                )

                st.session_state.matches = matches


            except Exception as error:

                st.error(
                    f"❌ Error while matching internships: {error}"
                )

                st.session_state.matches = None


    # ========================================================
    # MATCH RESULTS
    # ========================================================

    if st.session_state.matches:

        matches = st.session_state.matches


        st.success(
            f"🎉 {len(matches)} internship matches found!"
        )


        for index, match in enumerate(
            matches,
            start=1
        ):

            score = match[
                "compatibility_score"
            ]


            # ------------------------------------------------
            # JOB CARD
            # ------------------------------------------------

            with st.container(border=True):

                st.subheader(
                    f"{index}. {match['title']}"
                )


                st.write(
                    f"🏢 **Company:** "
                    f"{match['company']}"
                )


                st.write(
                    f"📍 **Location:** "
                    f"{match['location']}"
                )


                st.write(
                    "### ✦ Compatibility Score"
                )


                st.progress(
                    min(score / 100, 1.0)
                )


<<<<<<< HEAD
        os.remove(temp_path)

# --------------------------------------------------
# Internship Recommendations
# --------------------------------------------------

if st.session_state.profile is not None:

    st.subheader("🎯 Internship Recommendations")

    if st.button("Find Suitable Internships"):

        with st.spinner(
            "Finding suitable internships..."
        ):

            matches = match_candidate_to_jobs(
                st.session_state.profile,
                top_k=5
            )

        if not matches:

            st.warning(
                "No suitable internships found."
            )

        else:

            for index, match in enumerate(
                matches,
                start=1
            ):

                st.markdown(
                    f"### {index}. {match['title']}"
                )

                st.write(
                    f"**Company:** "
                    f"{match['company']}"
                )

                st.write(
                    f"**Location:** "
                    f"{match['location']}"
                )

                st.markdown(
                    "**AI Analysis:**"
                )

                st.write(
                    match["analysis"]
                )

                st.divider()
=======
                st.metric(
                    "Match Score",
                    f"{score}%"
                )


                # ------------------------------------------------
                # AI ANALYSIS
                # ------------------------------------------------

                with st.expander(
                    "🤖 View AI Matching Analysis"
                ):

                    st.write(
                        match["analysis"]
                    )


            st.write("")


    elif st.session_state.matches == []:

        st.warning(
            "No suitable internships found."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "✦ CareerAI | Intelligent internship matching "
    "powered by Python • RAG • ChromaDB • AI"
)
>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
