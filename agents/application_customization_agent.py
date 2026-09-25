import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# OPENROUTER / LLM SETUP
# ============================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "openai/gpt-4o-mini"
)

def candidate_to_text(candidate):
    """
    Convert the structured CandidateProfile into
    readable text for the LLM.
    """

    education_text = []

    for education in candidate.education:

        education_text.append(
            f"- Degree: {education.degree}; "
            f"Institution: {education.institution}; "
            f"Year: {education.year}"
        )

    experience_text = []

    for experience in candidate.experience:

        experience_text.append(
            f"- Role: {experience.role}; "
            f"Company: {experience.company}; "
            f"Duration: {experience.duration}; "
            f"Description: {experience.description}"
        )

    project_text = []

    for project in candidate.projects:

        project_text.append(
            f"- Project: {project.name}; "
            f"Description: {project.description}; "
            f"Technologies: "
            f"{', '.join(project.technologies)}"
        )

    return f"""
Candidate Name:
{candidate.name}

Email:
{candidate.email}

Phone:
{candidate.phone}

Skills:
{", ".join(candidate.skills)}

Education:
{chr(10).join(education_text)}

Experience:
{chr(10).join(experience_text)}

Projects:
{chr(10).join(project_text)}

Certifications:
{", ".join(candidate.certifications)}

Career Interests:
{", ".join(candidate.career_interests)}
"""

def job_to_text(job):
    """
    Convert the selected internship dictionary into
    readable text for the LLM.
    """

    return f"""
Job ID:
{job.get("job_id", "")}

Job Title:
{job.get("job_title", "")}

Company:
{job.get("company", "")}

Location:
{job.get("location", "")}

Job Type:
{job.get("job_type", "")}

Job Description:
{job.get("job_description", "")}

Responsibilities:
{", ".join(job.get("responsibilities", []))}

Required Skills:
{", ".join(job.get("required_skills", []))}

Preferred Skills:
{", ".join(job.get("preferred_skills", []))}

Qualification:
{job.get("qualification", "")}

Experience Requirements:
{job.get("experience_requirements", "")}

Education Requirements:
{job.get("education_requirements", "")}
"""

def extract_job_keywords(job):
    """
    Collect important keywords from the selected
    internship posting.
    """

    keywords = []

    keywords.extend(
        job.get("required_skills", [])
    )

    keywords.extend(
        job.get("preferred_skills", [])
    )

    responsibilities = job.get(
        "responsibilities",
        []
    )

    keywords.extend(
        responsibilities
    )

    # Remove duplicates while preserving order
    unique_keywords = []

    seen = set()

    for keyword in keywords:

        keyword_clean = str(
            keyword
        ).strip()

        if not keyword_clean:
            continue

        key = keyword_clean.lower()

        if key not in seen:

            seen.add(key)

            unique_keywords.append(
                keyword_clean
            )

    return unique_keywords

def generate_customized_resume(
    candidate,
    job
):
    """
    Generate a role-specific resume using only
    information available in the candidate profile.
    """

    candidate_text = candidate_to_text(
        candidate
    )

    job_text = job_to_text(
        job
    )

    job_keywords = extract_job_keywords(
        job
    )

    prompt = f"""
You are a Resume Customization Agent.

Your task is to customize a student's resume
for a specific internship.

==================================================
CANDIDATE PROFILE
==================================================

{candidate_text}

==================================================
SELECTED INTERNSHIP
==================================================

{job_text}

==================================================
IMPORTANT JOB KEYWORDS
==================================================

{job_keywords}

==================================================
INSTRUCTIONS
==================================================

Create a tailored resume for this internship.

1. Identify the candidate's most relevant skills.

2. Prioritize skills that are relevant to the
   internship.

3. Identify the candidate's most relevant
   projects.

4. Identify relevant education and experience.

5. Highlight relevant certifications.

6. Prioritize the resume sections according
   to the internship requirements.

7. Suggest improvements to project and
   experience bullet points.

8. Naturally incorporate relevant keywords
   from the job posting.

9. Use keywords only when they are supported
   by the candidate's actual profile.

10. NEVER invent:
    - Skills
    - Projects
    - Experience
    - Certifications
    - Achievements
    - Education
    - Technologies

11. Do not claim that the candidate has used
    a technology unless it appears in the
    candidate profile.

12. Do not create fake numbers or achievements.

13. Do not change factual information.

==================================================
OUTPUT FORMAT
==================================================

TAILORED RESUME

Professional Summary:
Write a short summary specifically relevant
to the selected internship.

Relevant Skills:
List the candidate's actual skills that are
most relevant to the internship.

Education:
List relevant education from the candidate.

Relevant Experience:
List relevant experience from the candidate.
If no formal experience exists, do not invent any.

Relevant Projects:
Select the projects most relevant to the role.

Certifications:
List relevant certifications.

Relevant Achievements:
Mention only achievements actually present
in the candidate profile.

==================================================

RESUME IMPROVEMENT SUGGESTIONS

Section Priority:
Explain which resume sections should receive
the most attention for this role.

Bullet Point Improvements:
Suggest improved wording for existing project
or experience descriptions.

Job Keywords to Include:
List important keywords from the job posting
that are supported by the candidate's profile.

Missing Keywords:
List important job keywords that the candidate
does not currently demonstrate.

==================================================

IMPORTANT:
The customized resume must remain truthful.
Do not invent information just to improve the
candidate's match.
"""
    
    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[

            {
                "role": "system",
                "content": (
                    "You are an expert resume "
                    "customization assistant. "
                    "You must keep all candidate "
                    "information truthful."
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content

def generate_cover_letter(
    candidate,
    job
):
    """
    Generate a role-specific cover letter
    using only verified candidate information.
    """

    candidate_text = candidate_to_text(
        candidate
    )

    job_text = job_to_text(
        job
    )

    prompt = f"""
You are a professional Cover Letter
Customization Agent.

Create a personalized cover letter for
the selected internship.

==================================================
CANDIDATE PROFILE
==================================================

{candidate_text}

==================================================
SELECTED INTERNSHIP
==================================================

{job_text}

==================================================
INSTRUCTIONS
==================================================

Write a professional and personalized
cover letter.

The cover letter should:

1. Address the selected internship.

2. Mention the company name.

3. Explain the candidate's interest in
   the internship.

4. Connect the candidate's actual education
   with the role.

5. Connect relevant candidate skills
   with the internship requirements.

6. Mention relevant projects.

7. Highlight relevant strengths.

8. Explain why the candidate's background
   is relevant to the role.

9. Maintain a professional tone.

10. Keep the letter concise.

11. Use only information from the candidate
    profile.

12. NEVER invent:
    - Skills
    - Projects
    - Experience
    - Certifications
    - Achievements
    - Technologies

13. Do not claim professional experience
    if the candidate only has academic or
    project experience.

==================================================
OUTPUT FORMAT
==================================================

Cover Letter

[Professional cover letter]

==================================================

PERSONALIZATION NOTES

Explain briefly:

- Which candidate skills were highlighted.
- Which project was highlighted.
- Which job requirements were connected
  to the candidate's background.
"""
    
    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[

            {
                "role": "system",
                "content": (
                    "You are an expert professional "
                    "cover letter writer. "
                    "Never invent candidate information."
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    return response.choices[0].message.content

def customize_application(
    candidate,
    job
):
    """
    Main M3.2 function.

    Generates both:
    1. Customized resume
    2. Customized cover letter
    """

    resume = generate_customized_resume(
        candidate,
        job
    )

    cover_letter = generate_cover_letter(
        candidate,
        job
    )

    return {
        "resume": resume,
        "cover_letter": cover_letter
    }
