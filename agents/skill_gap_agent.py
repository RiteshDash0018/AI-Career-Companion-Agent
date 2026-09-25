import os
import re

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. OPENROUTER / LLM SETUP
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


# ============================================================
# 2. TEXT NORMALIZATION
# ============================================================

def normalize(text):
    """
    Convert text into a simple comparable format.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Replace special characters with spaces
    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# 3. RELATED SKILL GROUPS
# ============================================================

RELATED_SKILLS = {

    "machine learning": [
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "keras",
        "xgboost",
        "lightgbm"
    ],

    "deep learning": [
        "tensorflow",
        "pytorch",
        "keras",
        "resnet",
        "cnn",
        "lstm",
        "gru",
        "transformer"
    ],

    "data science": [
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn",
        "sql",
        "statistics"
    ],

    "data analysis": [
        "pandas",
        "numpy",
        "sql",
        "matplotlib",
        "excel",
        "statistics"
    ],

    "frontend development": [
        "html",
        "css",
        "javascript",
        "react",
        "angular",
        "vue"
    ],

    "web development": [
        "html",
        "css",
        "javascript",
        "react",
        "django",
        "flask",
        "node.js",
        "php"
    ],

    "backend development": [
        "python",
        "java",
        "node.js",
        "django",
        "flask",
        "spring",
        "sql",
        "mongodb"
    ],

    "cloud computing": [
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes"
    ],

    "devops": [
        "docker",
        "kubernetes",
        "aws",
        "jenkins",
        "git",
        "linux",
        "terraform"
    ],

    "cybersecurity": [
        "network security",
        "ethical hacking",
        "linux",
        "penetration testing",
        "siem",
        "wireshark",
        "cryptography"
    ],

    "network security": [
        "cybersecurity",
        "ethical hacking",
        "wireshark",
        "linux",
        "firewalls",
        "tcp/ip"
    ]
}


# ============================================================
# 4. GET CANDIDATE INFORMATION
# ============================================================

def get_candidate_information(candidate):
    """
    Extract relevant information from the student's
    structured CandidateProfile.
    """

    # --------------------------------------------------------
    # Candidate skills
    # --------------------------------------------------------

    candidate_skills = list(candidate.skills)

    # Add technologies used in projects
    project_technologies = []

    for project in candidate.projects:

        project_technologies.extend(
            project.technologies
        )

    # Combine skills and project technologies
    all_skills = list(
        set(
            candidate_skills +
            project_technologies
        )
    )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education = []

    for item in candidate.education:

        education.append({
            "degree": item.degree,
            "institution": item.institution,
            "year": item.year
        })

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    experience = []

    for item in candidate.experience:

        experience.append({
            "company": item.company,
            "role": item.role,
            "duration": item.duration,
            "description": item.description
        })

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    projects = []

    for project in candidate.projects:

        projects.append({
            "name": project.name,
            "description": project.description,
            "technologies": project.technologies
        })

    # --------------------------------------------------------
    # Final candidate information
    # --------------------------------------------------------

    return {

        "skills": all_skills,

        "education": education,

        "experience": experience,

        "projects": projects,

        "certifications": candidate.certifications,

        "career_interests": candidate.career_interests
    }


# ============================================================
# 5. GET JOB REQUIREMENTS
# ============================================================

def get_job_requirements(job):
    """
    Extract all relevant requirements from the selected
    internship/job.
    """

    return {

        "required_skills": job.get(
            "required_skills",
            []
        ),

        "preferred_skills": job.get(
            "preferred_skills",
            []
        ),

        "qualification": job.get(
            "qualification",
            ""
        ),

        "experience_requirements": job.get(
            "experience_requirements",
            ""
        ),

        "education_requirements": job.get(
            "education_requirements",
            ""
        ),

        "responsibilities": job.get(
            "responsibilities",
            []
        )
    }


# ============================================================
# 6. COMPARE SKILLS
# ============================================================

def compare_skills(
    candidate_skills,
    job_skills
):
    """
    Compare candidate skills with job skills.

    Returns:
        matched skills
        missing skills
    """

    candidate_normalized = {
        normalize(skill)
        for skill in candidate_skills
        if skill and normalize(skill)
    }

    matched = []

    missing = []

    for skill in job_skills:

        normalized_skill = normalize(skill)

        if not normalized_skill:
            continue

        if normalized_skill in candidate_normalized:

            matched.append(skill)

        else:

            missing.append(skill)

    return matched, missing


# ============================================================
# 7. FIND PARTIALLY DEMONSTRATED SKILLS
# ============================================================

def find_partial_skills(
    candidate_skills,
    missing_job_skills
):
    """
    Identify job skills that are not explicitly present
    but are supported by related candidate skills.

    Example:

    Job:
        Deep Learning

    Candidate:
        TensorFlow

    Result:
        Deep Learning -> Partially Demonstrated
        Evidence -> TensorFlow
    """

    candidate_skills_normalized = {
        normalize(skill)
        for skill in candidate_skills
        if skill and normalize(skill)
    }

    partial_skills = []

    for job_skill in missing_job_skills:

        normalized_job_skill = normalize(
            job_skill
        )

        related_skills = RELATED_SKILLS.get(
            normalized_job_skill,
            []
        )

        matched_related_skills = []

        for candidate_skill in candidate_skills_normalized:

            if candidate_skill in related_skills:

                matched_related_skills.append(
                    candidate_skill
                )

        if matched_related_skills:

            partial_skills.append({
                "skill": job_skill,
                "evidence": matched_related_skills
            })

    return partial_skills


# ============================================================
# 8. EDUCATION ANALYSIS
# ============================================================

def analyze_education(
    candidate,
    job
):
    """
    Compare candidate education with job education
    requirements.
    """

    if not candidate.education:

        return (
            "Education information is missing "
            "from the candidate profile."
        )

    job_education = normalize(
        job.get(
            "education_requirements",
            ""
        )
    )

    if not job_education:

        return (
            "No specific education requirement "
            "was provided for this internship."
        )

    # Common education keywords
    education_keywords = [

        "b.tech",
        "btech",

        "b.e",
        "be",

        "bachelor",

        "m.tech",
        "mtech",

        "master",

        "computer science",

        "information technology",

        "software engineering",

        "artificial intelligence",

        "machine learning",

        "data science",

        "electronics",

        "electrical"
    ]

    for education in candidate.education:

        degree = normalize(
            education.degree
        )

        if not degree:
            continue

        # Direct match
        if degree in job_education:

            return (
                f"The candidate's "
                f"{education.degree} "
                f"matches the internship's "
                f"education requirement."
            )

        # Keyword-based match
        matched_keywords = []

        for keyword in education_keywords:

            if (
                keyword in degree
                and keyword in job_education
            ):

                matched_keywords.append(
                    keyword
                )

        if matched_keywords:

            return (
                f"The candidate's "
                f"{education.degree} "
                f"is relevant to the internship's "
                f"education requirement."
            )

    return (
        "The candidate's education does not clearly "
        "match the stated education requirement."
    )


# ============================================================
# 9. EXPERIENCE ANALYSIS
# ============================================================

def analyze_experience(
    candidate,
    job
):
    """
    Compare candidate experience with job
    experience requirements.
    """

    requirement = normalize(
        job.get(
            "experience_requirements",
            ""
        )
    )

    # No experience requirement
    if not requirement:

        return (
            "No specific experience requirement "
            "was provided."
        )

    # Fresher-friendly role
    if (
        "fresher" in requirement
        or "0-1" in requirement
        or "entry" in requirement
        or "no experience" in requirement
    ):

        return (
            "No major experience gap. "
            "The internship accepts fresher "
            "or entry-level candidates."
        )

    # Experience required but candidate has none
    if not candidate.experience:

        return (
            "Experience gap identified. "
            "The internship requires experience, "
            "but no formal experience is present "
            "in the candidate profile."
        )

    # Candidate has experience
    return (
        "The candidate has experience that can "
        "be compared with the role requirements."
    )


# ============================================================
# 10. QUALIFICATION ANALYSIS
# ============================================================

def analyze_qualification(
    candidate,
    job
):
    """
    Compare candidate education/certifications
    with job qualification requirements.
    """

    qualification = normalize(
        job.get(
            "qualification",
            ""
        )
    )

    if not qualification:

        return (
            "No specific qualification requirement "
            "was provided."
        )

    candidate_qualifications = []

    # Add education
    for education in candidate.education:

        if education.degree:

            candidate_qualifications.append(
                normalize(
                    education.degree
                )
            )

    # Add certifications
    for certification in candidate.certifications:

        if certification:

            candidate_qualifications.append(
                normalize(
                    certification
                )
            )

    if not candidate_qualifications:

        return (
            "Qualification gap cannot be fully assessed "
            "because education and certification "
            "information is missing."
        )

    # Direct qualification matching
    for candidate_qualification in candidate_qualifications:

        if (
            candidate_qualification
            in qualification
        ):

            return (
                "The candidate's qualification "
                "matches the internship requirement."
            )

        # Check important words
        qualification_words = [
            word
            for word in candidate_qualification.split()
            if len(word) > 2
        ]

        if any(
            word in qualification
            for word in qualification_words
        ):

            return (
                "The candidate's qualification "
                "appears relevant to the internship."
            )

    return (
        "The candidate's qualification does not "
        "clearly match the stated requirement."
    )


# ============================================================
# 11. PROJECT AND TECHNOLOGY EVIDENCE
# ============================================================

def get_project_evidence(candidate):
    """
    Collect technologies and project descriptions
    that can provide evidence of a skill.
    """

    evidence = []

    for project in candidate.projects:

        for technology in project.technologies:

            evidence.append(
                technology
            )

        if project.description:

            evidence.append(
                project.description
            )

    return evidence


# ============================================================
# 12. COMPLETE DETERMINISTIC GAP ANALYSIS
# ============================================================

def analyze_skill_gaps(
    candidate,
    job
):
    """
    Perform deterministic skill-gap analysis before
    asking the LLM for explanations.
    """

    candidate_info = get_candidate_information(
        candidate
    )

    job_requirements = get_job_requirements(
        job
    )

    # --------------------------------------------------------
    # Required skills
    # --------------------------------------------------------

    required_matched, required_missing = compare_skills(
        candidate_info["skills"],
        job_requirements["required_skills"]
    )

    # --------------------------------------------------------
    # Preferred skills
    # --------------------------------------------------------

    preferred_matched, preferred_missing = compare_skills(
        candidate_info["skills"],
        job_requirements["preferred_skills"]
    )

    # --------------------------------------------------------
    # Partially demonstrated required skills
    # --------------------------------------------------------

    partial_skills = find_partial_skills(
        candidate_info["skills"],
        required_missing
    )

    # Skills already classified as partially demonstrated
    partial_skill_names = {
        normalize(item["skill"])
        for item in partial_skills
    }

    # Remove partially demonstrated skills
    # from critical missing skills
    critical_missing = [

        skill

        for skill in required_missing

        if normalize(skill)
        not in partial_skill_names
    ]

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education_gap = analyze_education(
        candidate,
        job
    )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    experience_gap = analyze_experience(
        candidate,
        job
    )

    # --------------------------------------------------------
    # Qualification
    # --------------------------------------------------------

    qualification_gap = analyze_qualification(
        candidate,
        job
    )

    # --------------------------------------------------------
    # Project evidence
    # --------------------------------------------------------

    project_evidence = get_project_evidence(
        candidate
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    result = {

        "matched_required_skills":
            required_matched,

        "critical_missing_skills":
            critical_missing,

        "matched_preferred_skills":
            preferred_matched,

        "preferred_skill_gaps":
            preferred_missing,

        "partially_demonstrated_skills":
            partial_skills,

        "experience_gap":
            experience_gap,

        "education_gap":
            education_gap,

        "qualification_gap":
            qualification_gap,

        "project_evidence":
            project_evidence
    }

    return result


# ============================================================
# 13. LLM-BASED GAP EXPLANATION
# ============================================================

def generate_gap_explanation(
    candidate,
    job,
    gap_analysis
):
    """
    Use the LLM to explain the identified gaps and
    generate personalized recommendations.
    """

    candidate_info = get_candidate_information(
        candidate
    )

    job_requirements = get_job_requirements(
        job
    )

    prompt = f"""
You are a Skill Gap Analysis Agent for an
AI-powered career assistant.

Your job is to compare a student's structured
profile with a selected internship.

========================
CANDIDATE PROFILE
========================

{candidate_info}

========================
JOB REQUIREMENTS
========================

{job_requirements}

========================
DETERMINISTIC GAP ANALYSIS
========================

{gap_analysis}

========================
YOUR TASK
========================

Analyze the candidate carefully.

1. Identify critical or missing skills.

2. Identify partially demonstrated skills.

Only classify a skill as partially demonstrated
when it is a REQUIRED skill that the candidate
does not explicitly list but has related
technologies, tools, projects or experience
that provide evidence of exposure to it.

Do NOT classify a missing PREFERRED skill as
partially demonstrated.

For example:

Required skill:
Deep Learning

Candidate skill:
TensorFlow

Result:
Partially Demonstrated - Deep Learning

However, if Scikit-learn is only a preferred
skill and the candidate does not have it, classify
it only as a Preferred Skill Gap.

3. Identify preferred skill gaps.

4. Identify experience gaps.

5. Identify education gaps.

6. Identify qualification gaps.

7. Consider projects, tools, technologies and
certifications when evaluating the candidate.

8. Explain why each important missing or partially
demonstrated skill is important for the selected
internship.

9. Give personalized recommendations for closing
the identified gaps.

10. Suggest practical learning activities,
practice areas or projects.

11. Recommendations should be relevant to the
selected internship.

12. NEVER invent candidate information.

Do not invent:
- Skills
- Projects
- Experience
- Education
- Certifications
- Achievements
- Job responsibilities

Only use information provided in the candidate
profile.

========================
OUTPUT FORMAT
========================

Critical/Missing Skills:

- List each truly missing required skill.
- If none exist, write:
  "None identified."

Partially Demonstrated Skills:

- List the skill.
- Mention the candidate evidence.
- If none exist, write:
  "None identified."

Preferred Skills:

- List missing preferred skills.
- If none exist, write:
  "None identified."

Experience Gaps:

- Explain whether the candidate meets the
  experience requirement.

Qualification/Education Gaps:

- Explain whether the candidate's education
  and qualifications match the role.

Why These Skills Matter:

- Explain why the important missing or
  partially demonstrated skills matter
  for this internship.

Personalized Recommendations:

- Give practical recommendations specifically
  for this candidate.

Suggested Projects or Practice:

- Suggest projects or practice activities
  that help close the identified gaps.

Keep the answer clear, practical and concise.
"""

    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[

            {
                "role": "system",

                "content": (
                    "You are an expert career "
                    "skill-gap analysis assistant. "
                    "You provide accurate, "
                    "evidence-based and personalized "
                    "career guidance."
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


# ============================================================
# 14. MAIN SKILL GAP ANALYSIS FUNCTION
# ============================================================

def skill_gap_analysis(
    candidate,
    job
):
    """
    Main function used by the application.

    Input:
        candidate -> CandidateProfile
        job       -> selected internship dictionary

    Output:
        deterministic analysis
        LLM explanation
    """

    # Step 1:
    # Perform rule-based comparison
    gap_analysis = analyze_skill_gaps(
        candidate,
        job
    )

    # Step 2:
    # Ask LLM to explain the gaps and
    # generate recommendations
    explanation = generate_gap_explanation(
        candidate,
        job,
        gap_analysis
    )

    # Step 3:
    # Return both results
    return {

        "analysis":
            gap_analysis,

        "explanation":
            explanation
    }