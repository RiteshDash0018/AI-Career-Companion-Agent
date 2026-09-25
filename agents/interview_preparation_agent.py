import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "openai/gpt-4o-mini"
)


# ==========================================================
# CANDIDATE PROFILE -> TEXT
# ==========================================================

def candidate_to_text(candidate):

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
            f"Technologies: {', '.join(project.technologies)}"
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


# ==========================================================
# JOB POSTING -> TEXT
# ==========================================================

def job_to_text(job):

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


# ==========================================================
# SKILL GAP ANALYSIS -> TEXT
# ==========================================================

def skill_gap_to_text(skill_gap):

    if not skill_gap:
        return "No skill gap analysis was provided."

    matched_required = skill_gap.get(
        "matched_required_skills",
        []
    )

    missing_required = skill_gap.get(
        "missing_required_skills",
        []
    )

    partial_skills = skill_gap.get(
        "partial_skills",
        []
    )

    matched_preferred = skill_gap.get(
        "matched_preferred_skills",
        []
    )

    missing_preferred = skill_gap.get(
        "missing_preferred_skills",
        []
    )

    education_analysis = skill_gap.get(
        "education_analysis",
        ""
    )

    experience_analysis = skill_gap.get(
        "experience_analysis",
        ""
    )

    qualification_analysis = skill_gap.get(
        "qualification_analysis",
        ""
    )

    project_evidence = skill_gap.get(
        "project_evidence",
        []
    )

    return f"""
MATCHED REQUIRED SKILLS:
{", ".join(matched_required)}

MISSING REQUIRED SKILLS:
{", ".join(missing_required)}

PARTIALLY DEMONSTRATED REQUIRED SKILLS:
{partial_skills}

MATCHED PREFERRED SKILLS:
{", ".join(matched_preferred)}

MISSING PREFERRED SKILLS:
{", ".join(missing_preferred)}

EDUCATION ANALYSIS:
{education_analysis}

EXPERIENCE ANALYSIS:
{experience_analysis}

QUALIFICATION ANALYSIS:
{qualification_analysis}

PROJECT EVIDENCE:
{project_evidence}
"""


# ==========================================================
# GENERATE INTERVIEW QUESTIONS
# ==========================================================

def generate_interview_questions(
    candidate,
    job,
    skill_gap=None
):

    candidate_text = candidate_to_text(candidate)

    job_text = job_to_text(job)

    skill_gap_text = skill_gap_to_text(skill_gap)

    prompt = f"""
You are an Interview Preparation Agent.

Prepare an internship candidate for a specific interview.

==================================================
CANDIDATE PROFILE
==================================================

{candidate_text}

==================================================
SELECTED INTERNSHIP
==================================================

{job_text}

==================================================
SKILL GAP ANALYSIS
==================================================

{skill_gap_text}

==================================================
INTERVIEW QUESTION REQUIREMENTS
==================================================

Generate five categories of interview questions:

1. TECHNICAL QUESTIONS
2. RESUME-BASED QUESTIONS
3. PROJECT-BASED QUESTIONS
4. ROLE-SPECIFIC QUESTIONS
5. HR / GENERAL QUESTIONS

Generate approximately 5 questions for each category.

For EVERY question provide:

Question:
Why this question may be asked:
What the interviewer is evaluating:
Preparation guidance:

==================================================
IMPORTANT ACCURACY RULES
==================================================

1. Use the actual candidate profile.

2. Use the actual selected internship.

3. Use the actual job requirements.

4. Use the actual skill-gap analysis.

5. Do NOT call a matched skill a skill gap.

6. Do NOT say that the candidate lacks a skill if the
   skill-gap analysis shows that the skill is matched.

7. Missing required skills may be used as areas for
   technical preparation.

8. Missing preferred skills may be used as additional
   preparation topics.

9. Partially demonstrated skills may be used for
   deeper preparation.

10. Do NOT invent candidate experience.

11. Do NOT invent projects.

12. Do NOT invent certifications.

13. Do NOT invent achievements.

14. Do NOT invent technologies used in projects.

15. Do NOT assume a particular machine learning algorithm
    was used unless the candidate profile explicitly states it.

16. Do NOT assume a particular preprocessing technique
    was used unless the candidate profile explicitly states it.

17. Do NOT assume a particular dataset was used unless
    the candidate profile explicitly states it.

18. Do NOT assume particular evaluation metrics were used
    unless the candidate profile explicitly states them.

19. Do NOT assume professional experience if only academic
    or project experience is provided.

20. If a project detail is unknown, phrase the question
    conditionally.

For example:

GOOD:
"What machine learning approach did you use in your project,
if applicable?"

GOOD:
"How did you evaluate your project, if you performed
model evaluation?"

BAD:
"What Random Forest model did you use?"

if Random Forest was never mentioned.

==================================================
PROJECT QUESTION RULE
==================================================

Project questions should focus first on information that
is actually known from the candidate profile.

Known project information may include:

- Project name
- Project description
- Technologies

For unknown information, ask the candidate to explain it
rather than assuming that it happened.

Examples:

"Can you explain the problem your project was designed
to solve?"

"What technologies did you use in the project?"

"What challenges did you face, if any?"

"What machine learning approach did you use, if applicable?"

"How did you evaluate your project, if you performed
model evaluation?"

==================================================
OUTPUT FORMAT
==================================================

### 1. TECHNICAL QUESTIONS

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:
...

Question 5:
...

### 2. RESUME-BASED QUESTIONS

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:
...

Question 5:
...

### 3. PROJECT-BASED QUESTIONS

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:
...

Question 5:
...

### 4. ROLE-SPECIFIC QUESTIONS

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:
...

Question 5:
...

### 5. HR / GENERAL QUESTIONS

Question 1:
...

Question 2:
...

Question 3:
...

Question 4:
...

Question 5:
...

Keep the questions realistic, useful, and personalized.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert internship interview "
                    "preparation assistant. "
                    "You must use only supported candidate "
                    "information and must not invent facts."
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


# ==========================================================
# GENERATE REVISION TOPICS
# ==========================================================

def generate_revision_topics(
    candidate,
    job,
    skill_gap=None
):

    candidate_text = candidate_to_text(candidate)

    job_text = job_to_text(job)

    skill_gap_text = skill_gap_to_text(skill_gap)

    prompt = f"""
You are an Interview Revision Planning Agent.

Create a personalized revision plan for the candidate.

==================================================
CANDIDATE
==================================================

{candidate_text}

==================================================
INTERNSHIP
==================================================

{job_text}

==================================================
SKILL GAP ANALYSIS
==================================================

{skill_gap_text}

==================================================
TASK
==================================================

Identify what the student should revise before the
interview.

Consider:

1. Required job skills
2. Missing required skills
3. Partially demonstrated skills
4. Missing preferred skills
5. Expected technical knowledge
6. Job responsibilities
7. Candidate projects
8. Candidate experience
9. Candidate education

==================================================
CRITICAL CONSISTENCY CHECK
==================================================

Before generating revision topics, compare every proposed
revision topic against the candidate's actual skills.

If the candidate profile contains a skill:

- Do NOT describe that skill as missing.
- Do NOT say that the candidate has not demonstrated it.
- Do NOT recommend learning it from scratch.

For example:

If SQL appears in the candidate's skills, SQL must NOT
be described as a missing skill.

SQL may still be recommended for revision or strengthening,
but the wording must be:

"Review and strengthen SQL knowledge."

NOT:

"Learn SQL because the candidate has not demonstrated it."

==================================================
SKILL GAP RULES
==================================================

1. If a skill appears under MATCHED REQUIRED SKILLS,
   do NOT describe it as a missing required skill.

2. If a skill appears under MATCHED PREFERRED SKILLS,
   do NOT describe it as a missing preferred skill.

3. Only skills listed under MISSING REQUIRED SKILLS
   should be described as missing required skills.

4. Only skills listed under MISSING PREFERRED SKILLS
   should be described as missing preferred skills.

5. Partially demonstrated skills should be presented as
   topics that need deeper preparation.

6. A matched skill can still be a revision topic because
   interview preparation may require strengthening it.

7. When a matched skill is recommended for revision,
   explicitly say that the candidate already demonstrates
   the skill.

For example:

"SQL is already listed among the candidate's skills.
Review joins, aggregation, subqueries, and query optimization
to strengthen interview readiness."

Do NOT say:

"SQL is missing."

==================================================
PROJECT ACCURACY RULES
==================================================

Only state project details that appear in the candidate profile.

Do NOT assume the candidate used:

- A particular algorithm
- A particular dataset
- A particular preprocessing technique
- A particular evaluation metric
- A particular deployment method
- A particular tool
- A particular architecture

unless it is explicitly present in the candidate profile.

If these details are not provided, phrase them as possible
areas to review.

GOOD:

"If applicable, review the dataset and preprocessing steps
actually used in the project."

GOOD:

"If model evaluation was performed, review the metrics that
were actually used."

BAD:

"The candidate used normalization and F1 score."

when those details are not provided.

==================================================
EXPERIENCE ACCURACY
==================================================

Do not invent professional experience.

If the candidate has only academic or project experience,
prepare them using those experiences.

==================================================
OUTPUT FORMAT
==================================================

### HIGH PRIORITY REVISION TOPICS

Topic:
...

Why to revise:
...

What to study:
...

How it may appear in the interview:
...

### MEDIUM PRIORITY REVISION TOPICS

Topic:
...

Why to revise:
...

What to study:
...

How it may appear in the interview:
...

### PROJECT REVISION TOPICS

Topic:
...

Why to revise:
...

What to study:
...

How it may appear in the interview:
...

### ROLE-SPECIFIC REVISION TOPICS

Topic:
...

Why to revise:
...

What to study:
...

How it may appear in the interview:
...

### HR / GENERAL PREPARATION

Topic:
...

Why to revise:
...

What to study:
...

How it may appear in the interview:
...

Only include topics that are relevant to this candidate
and this internship.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert interview revision "
                    "planning assistant. "
                    "Maintain strict consistency with the "
                    "candidate profile and skill-gap analysis. "
                    "Never describe an existing candidate skill "
                    "as missing."
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


# ==========================================================
# COMPLETE INTERVIEW PREPARATION
# ==========================================================

def prepare_interview(
    candidate,
    job,
    skill_gap=None
):

    interview_questions = generate_interview_questions(
        candidate,
        job,
        skill_gap
    )

    revision_topics = generate_revision_topics(
        candidate,
        job,
        skill_gap
    )

    return {
        "interview_questions": interview_questions,
        "revision_topics": revision_topics
    }


# ==========================================================
# MOCK INTERVIEW - GENERATE ONE QUESTION
# ==========================================================

def generate_mock_question(
    candidate,
    job,
    skill_gap=None,
    previous_questions=None
):

    candidate_text = candidate_to_text(candidate)

    job_text = job_to_text(job)

    skill_gap_text = skill_gap_to_text(skill_gap)

    previous_questions = previous_questions or []

    prompt = f"""
You are conducting a mock internship interview.

==================================================
CANDIDATE
==================================================

{candidate_text}

==================================================
INTERNSHIP
==================================================

{job_text}

==================================================
SKILL GAP
==================================================

{skill_gap_text}

==================================================
PREVIOUS QUESTIONS
==================================================

{previous_questions}

==================================================
TASK
==================================================

Generate ONE interview question.

Choose one type:

- Technical
- Resume-based
- Project-based
- Role-specific
- HR/general

Do not repeat a previous question.

==================================================
ACCURACY RULES
==================================================

- Do not invent candidate experience.
- Do not invent projects.
- Do not invent technologies.
- Do not assume unknown project details.
- Do not call matched skills missing.
- If asking about an unknown project detail,
  phrase the question conditionally.

==================================================
OUTPUT
==================================================

Question Type:
...

Question:
...

Why it is being asked:
...

Preparation Guidance:
...
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional internship interviewer. "
                    "Ask accurate, personalized questions without "
                    "inventing candidate information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


# ==========================================================
# MOCK INTERVIEW - EVALUATE ANSWER
# ==========================================================

def evaluate_mock_answer(
    question,
    answer,
    candidate,
    job
):

    candidate_text = candidate_to_text(candidate)

    job_text = job_to_text(job)

    prompt = f"""
You are evaluating a student's answer during a mock
internship interview.

==================================================
CANDIDATE
==================================================

{candidate_text}

==================================================
INTERNSHIP
==================================================

{job_text}

==================================================
INTERVIEW QUESTION
==================================================

{question}

==================================================
STUDENT ANSWER
==================================================

{answer}

==================================================
TASK
==================================================

Evaluate the student's answer.

Consider:

1. Technical correctness
2. Relevance
3. Clarity
4. Structure
5. Understanding
6. Communication

==================================================
IMPORTANT
==================================================

Do not expect the student to claim experience that is
not present in the candidate profile.

Do not invent achievements or professional experience
for the student.

If the student gives an answer based on academic or
project experience, evaluate it accordingly.

==================================================
OUTPUT
==================================================

### ANSWER EVALUATION

Strengths:
- ...

Areas for Improvement:
- ...

Technical Accuracy:
...

Relevance:
...

Clarity:
...

Suggested Improved Answer:
...

Interview Tip:
...

The suggested improved answer must remain truthful and
consistent with the candidate profile.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert internship interviewer "
                    "who provides constructive, accurate, and "
                    "truthful feedback."
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