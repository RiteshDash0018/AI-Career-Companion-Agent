import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from agents.job_matching_agent import match_candidate_to_jobs
from agents.skill_gap_agent import skill_gap_analysis
from agents.application_customization_agent import (
    customize_application
)
from agents.interview_preparation_agent import (
    prepare_interview
)


# ==========================================================
# OPENROUTER SETUP
# ==========================================================

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
# LOAD JOB DATA
# ==========================================================

def load_jobs():
    """
    Load all internship jobs from data/jobs.json.
    """

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================================
# FIND JOB BY ID
# ==========================================================

def get_job_by_id(job_id):

    jobs = load_jobs()

    for job in jobs:

        if job.get("job_id") == job_id:
            return job

    return None


# ==========================================================
# CONVERT CANDIDATE TO TEXT
# ==========================================================

def candidate_to_text(candidate):

    education = []

    for item in candidate.education:

        education.append(
            f"{item.degree} at "
            f"{item.institution} ({item.year})"
        )

    experience = []

    for item in candidate.experience:

        experience.append(
            f"{item.role} at {item.company} "
            f"({item.duration}) - "
            f"{item.description}"
        )

    projects = []

    for item in candidate.projects:

        projects.append(
            f"{item.name}: "
            f"{item.description}. "
            f"Technologies: "
            f"{', '.join(item.technologies)}"
        )

    return f"""
Candidate Name:
{candidate.name}

Skills:
{", ".join(candidate.skills)}

Education:
{"; ".join(education)}

Experience:
{"; ".join(experience)}

Projects:
{"; ".join(projects)}

Certifications:
{", ".join(candidate.certifications)}

Career Interests:
{", ".join(candidate.career_interests)}
"""


# ==========================================================
# CONVERT JOB TO TEXT
# ==========================================================

def job_to_text(job):

    responsibilities = job.get(
        "responsibilities",
        []
    )

    if isinstance(
        responsibilities,
        list
    ):
        responsibilities_text = "\n".join(
            f"- {item}"
            for item in responsibilities
        )
    else:
        responsibilities_text = str(
            responsibilities
        )

    required_skills = job.get(
        "required_skills",
        []
    )

    preferred_skills = job.get(
        "preferred_skills",
        []
    )

    if isinstance(
        required_skills,
        list
    ):
        required_skills_text = ", ".join(
            required_skills
        )
    else:
        required_skills_text = str(
            required_skills
        )

    if isinstance(
        preferred_skills,
        list
    ):
        preferred_skills_text = ", ".join(
            preferred_skills
        )
    else:
        preferred_skills_text = str(
            preferred_skills
        )

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

Description:
{job.get("job_description", "")}

Responsibilities:
{responsibilities_text}

Required Skills:
{required_skills_text}

Preferred Skills:
{preferred_skills_text}

Qualification:
{job.get("qualification", "")}

Experience Requirements:
{job.get("experience_requirements", "")}

Education Requirements:
{job.get("education_requirements", "")}
"""


# ==========================================================
# CONVERSATION MEMORY
# ==========================================================

class ConversationMemory:

    def __init__(self):

        self.messages = []

        self.selected_job_id = None

        self.selected_job = None

    # ------------------------------------------------------
    # Add user message
    # ------------------------------------------------------

    def add_user_message(self, message):

        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

    # ------------------------------------------------------
    # Add assistant message
    # ------------------------------------------------------

    def add_assistant_message(self, message):

        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )

    # ------------------------------------------------------
    # Select internship
    # ------------------------------------------------------

    def set_selected_job(self, job):

        if job:

            self.selected_job = job

            self.selected_job_id = job.get(
                "job_id"
            )

    # ------------------------------------------------------
    # Get recent conversation
    # ------------------------------------------------------

    def get_recent_history(
        self,
        limit=8
    ):

        return self.messages[-limit:]

    # ------------------------------------------------------
    # Clear memory
    # ------------------------------------------------------

    def clear(self):

        self.messages = []

        self.selected_job_id = None

        self.selected_job = None


# ==========================================================
# CONVERT MEMORY TO TEXT
# ==========================================================

def memory_to_text(memory):

    if not memory:

        return "No previous conversation."

    history = memory.get_recent_history()

    if not history:

        return "No previous conversation."

    lines = []

    for message in history:

        role = message["role"]

        content = message["content"]

        lines.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(lines)


# ==========================================================
# DETERMINE USER INTENT
# ==========================================================

def detect_intent(message):

    text = message.lower()

    # ------------------------------------------------------
    # Job recommendation
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "recommend",
            "recommendation",
            "suitable internship",
            "suitable internships",
            "internship for me",
            "internships for me",
            "job match",
            "matching jobs",
            "matching internships",
            "find internships",
            "find internship"
        ]
    ):

        return "job_recommendation"

    # ------------------------------------------------------
    # Skill gap
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "skill gap",
            "skill gaps",
            "missing skill",
            "missing skills",
            "what skills do i need",
            "what skills should i learn",
            "skills i lack"
        ]
    ):

        return "skill_gap"

    # ------------------------------------------------------
    # Resume
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "resume",
            "cv",
            "curriculum vitae"
        ]
    ):

        return "resume"

    # ------------------------------------------------------
    # Cover letter
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "cover letter",
            "coverletter"
        ]
    ):

        return "cover_letter"

    # ------------------------------------------------------
    # Interview
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "interview",
            "interview preparation",
            "prepare for interview",
            "interview questions",
            "mock interview"
        ]
    ):

        return "interview"

    # ------------------------------------------------------
    # Compare internships
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "compare",
            "comparison",
            "difference between"
        ]
    ):

        return "compare_jobs"

    # ------------------------------------------------------
    # Job requirements
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "requirement",
            "requirements",
            "qualification",
            "qualifications",
            "required skills",
            "preferred skills",
            "eligibility",
            "responsibilities"
        ]
    ):

        return "job_requirements"

    # ------------------------------------------------------
    # Career improvement
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "career advice",
            "career guidance",
            "improve my career",
            "improve my profile",
            "improve my skills",
            "what should i learn",
            "what should i improve",
            "employability"
        ]
    ):

        return "career_improvement"

    # ------------------------------------------------------
    # Application decision
    # ------------------------------------------------------

    if any(
        word in text
        for word in [
            "should i apply",
            "apply for",
            "application decision",
            "am i eligible",
            "do i qualify"
        ]
    ):

        return "application_decision"

    return "general"


# ==========================================================
# JOB RECOMMENDATION
# ==========================================================

def recommend_jobs(
    candidate,
    top_k=5
):

    """
    Use the existing M2.3 Job Matching Agent.

    Existing pipeline:

    Candidate
        ↓
    RAG retrieval
        ↓
    Compatibility scoring
        ↓
    LLM reasoning
        ↓
    Ranked internships
    """

    return match_candidate_to_jobs(
        candidate,
        top_k=top_k
    )


# ==========================================================
# SKILL GAP
# ==========================================================

def get_skill_gap(
    candidate,
    job
):

    return skill_gap_analysis(
        candidate,
        job
    )


# ==========================================================
# APPLICATION CUSTOMIZATION
# ==========================================================

def customize_job_application(
    candidate,
    job
):

    return customize_application(
        candidate,
        job
    )


# ==========================================================
# INTERVIEW PREPARATION
# ==========================================================

def get_interview_preparation(
    candidate,
    job,
    skill_gap
):

    return prepare_interview(
        candidate,
        job,
        skill_gap
    )


# ==========================================================
# BUILD CAREER CONTEXT
# ==========================================================

def build_context(
    candidate,
    user_message,
    memory=None,
    selected_job=None
):

    candidate_context = candidate_to_text(
        candidate
    )

    conversation_context = memory_to_text(
        memory
    )

    job_context = ""

    if selected_job:

        job_context = job_to_text(
            selected_job
        )

    return f"""
==================================================
CANDIDATE PROFILE
==================================================

{candidate_context}

==================================================
SELECTED INTERNSHIP
==================================================

{job_context}

==================================================
PREVIOUS CONVERSATION
==================================================

{conversation_context}

==================================================
CURRENT USER QUESTION
==================================================

{user_message}
"""


# ==========================================================
# GENERAL LLM RESPONSE
# ==========================================================

def generate_general_response(
    candidate,
    user_message,
    memory=None,
    selected_job=None
):

    context = build_context(
        candidate,
        user_message,
        memory,
        selected_job
    )

    prompt = f"""
You are CareerAI, a conversational career assistant.

Your job is to provide personalized internship
and career guidance based on the candidate profile
and conversation context.

{context}

Answer the user's question clearly and practically.

IMPORTANT RULES:

1. Personalize the answer using the candidate profile.

2. Maintain consistency with previous conversation.

3. If an internship is selected, use its actual information.

4. Do not invent candidate skills.

5. Do not invent projects.

6. Do not invent experience.

7. Do not invent certifications.

8. Do not invent achievements.

9. Do not invent job requirements.

10. Do not claim the candidate has a skill that is not
    present in the candidate profile.

11. If information is unavailable, say that it is not
    available rather than making it up.

12. Give actionable career guidance.

13. Do not make unsupported claims about companies.

14. Clearly distinguish:
    - Candidate facts
    - Job requirements
    - Suggestions

15. When discussing whether to apply, provide factual
    decision-support factors instead of making the
    decision for the candidate.

16. When comparing internships, compare documented
    characteristics without declaring one universally
    better or worse.

Provide a concise but useful response.
"""

    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful, accurate and "
                    "personalized career assistant."
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
# COMPARE TWO JOBS
# ==========================================================

def compare_jobs(
    candidate,
    job1,
    job2
):

    candidate_context = candidate_to_text(
        candidate
    )

    job1_context = job_to_text(
        job1
    )

    job2_context = job_to_text(
        job2
    )

    prompt = f"""
You are CareerAI.

Compare two internship opportunities for the
candidate using only the documented information.

CANDIDATE:
{candidate_context}

INTERNSHIP 1:
{job1_context}

INTERNSHIP 2:
{job2_context}

Compare:

1. Required skills
2. Preferred skills
3. Education requirements
4. Experience requirements
5. Responsibilities
6. Candidate's relevant skills
7. Candidate's relevant projects
8. Candidate's gaps
9. Preparation requirements
10. Important differences

Do not invent information.

Do not declare one internship universally better
or worse.

Do not make the application decision for the
candidate.

End with:

Decision Factors:
- List factual factors the candidate may consider.
"""

    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an objective internship "
                    "comparison assistant."
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
# MAIN CONVERSATIONAL ASSISTANT
# ==========================================================

def chat(
    candidate,
    user_message,
    memory=None
):

    if memory is None:

        memory = ConversationMemory()

    # ------------------------------------------------------
    # Store user message
    # ------------------------------------------------------

    memory.add_user_message(
        user_message
    )

    # ------------------------------------------------------
    # Detect intent
    # ------------------------------------------------------

    intent = detect_intent(
        user_message
    )

    selected_job = memory.selected_job

    response = None

    # ======================================================
    # JOB RECOMMENDATION
    # ======================================================

    if intent == "job_recommendation":

        results = recommend_jobs(
            candidate,
            top_k=5
        )

        if not results:

            response = (
                "No suitable internships were found "
                "from the current job knowledge base."
            )

        else:

            context = build_context(
                candidate,
                user_message,
                memory,
                selected_job
            )

            prompt = f"""
You are CareerAI.

The user wants internship recommendations.

CANDIDATE CONTEXT:

{context}

MATCHING AGENT RESULTS:

{results}

Explain the recommended internships.

For each internship explain:

- Job title
- Company
- Location
- Relevant matching skills
- Relevant candidate evidence
- Important requirements
- Known gaps

Do not invent information.

Do not provide a universal ranking.

Do not claim that one internship is objectively
the best.

Present the results as decision-support
information.
"""

            llm_response = client.chat.completions.create(

                model=LLM_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a personalized internship "
                            "recommendation assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2
            )

            response = (
                llm_response
                .choices[0]
                .message
                .content
            )

    # ======================================================
    # SKILL GAP
    # ======================================================

    elif intent == "skill_gap":

        if not selected_job:

            response = (
                "Please select an internship first so I "
                "can analyze your skill gaps for that role."
            )

        else:

            skill_gap = get_skill_gap(
                candidate,
                selected_job
            )

            prompt = f"""
You are CareerAI.

Explain the candidate's skill gaps for this internship.

CANDIDATE:

{candidate_to_text(candidate)}

JOB:

{job_to_text(selected_job)}

SKILL GAP ANALYSIS:

{skill_gap}

Explain:

1. Matched skills
2. Missing required skills
3. Partially demonstrated skills
4. Missing preferred skills
5. Education or experience gaps
6. Personalized improvement suggestions

Do not invent information.
"""

            llm_response = client.chat.completions.create(

                model=LLM_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a skill-gap career advisor."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2
            )

            response = (
                llm_response
                .choices[0]
                .message
                .content
            )

    # ======================================================
    # RESUME
    # ======================================================

    elif intent == "resume":

        if not selected_job:

            response = (
                "Please select an internship first so I "
                "can customize your resume for that role."
            )

        else:

            application = customize_job_application(
                candidate,
                selected_job
            )

            if isinstance(
                application,
                dict
            ):

                response = application.get(
                    "resume",
                    "Resume customization could not be generated."
                )

            else:

                response = str(
                    application
                )

    # ======================================================
    # COVER LETTER
    # ======================================================

    elif intent == "cover_letter":

        if not selected_job:

            response = (
                "Please select an internship first so I "
                "can create a role-specific cover letter."
            )

        else:

            application = customize_job_application(
                candidate,
                selected_job
            )

            if isinstance(
                application,
                dict
            ):

                response = application.get(
                    "cover_letter",
                    "Cover letter could not be generated."
                )

            else:

                response = str(
                    application
                )

    # ======================================================
    # INTERVIEW
    # ======================================================

    elif intent == "interview":

        if not selected_job:

            response = (
                "Please select an internship first so I "
                "can prepare an interview plan for that role."
            )

        else:

            skill_gap = get_skill_gap(
                candidate,
                selected_job
            )

            preparation = get_interview_preparation(
                candidate,
                selected_job,
                skill_gap
            )

            if isinstance(
                preparation,
                dict
            ):

                response = (
                    "INTERVIEW QUESTIONS\n\n"
                    + preparation.get(
                        "interview_questions",
                        ""
                    )
                    + "\n\n"
                    + "REVISION TOPICS\n\n"
                    + preparation.get(
                        "revision_topics",
                        ""
                    )
                )

            else:

                response = str(
                    preparation
                )

    # ======================================================
    # JOB REQUIREMENTS
    # ======================================================

    elif intent == "job_requirements":

        if not selected_job:

            response = (
                "Please select an internship first so I "
                "can show its requirements."
            )

        else:

            response = f"""
INTERNSHIP REQUIREMENTS

Job:
{selected_job.get("job_title", "")}

Company:
{selected_job.get("company", "")}

Required Skills:
{", ".join(
    selected_job.get(
        "required_skills",
        []
    )
)}

Preferred Skills:
{", ".join(
    selected_job.get(
        "preferred_skills",
        []
    )
)}

Qualification:
{selected_job.get("qualification", "")}

Education:
{selected_job.get("education_requirements", "")}

Experience:
{selected_job.get("experience_requirements", "")}

Responsibilities:
{chr(10).join(
    "- " + item
    for item in selected_job.get(
        "responsibilities",
        []
    )
)}
"""

    # ======================================================
    # CAREER IMPROVEMENT
    # ======================================================

    elif intent == "career_improvement":

        response = generate_general_response(
            candidate,
            user_message,
            memory,
            selected_job
        )

    # ======================================================
    # APPLICATION DECISION SUPPORT
    # ======================================================

    elif intent == "application_decision":

        if not selected_job:

            response = (
                "Please select an internship first. "
                "I can then show the documented match "
                "factors, requirements, and gaps to help "
                "you make an application decision."
            )

        else:

            skill_gap = get_skill_gap(
                candidate,
                selected_job
            )

            prompt = f"""
You are providing application decision support.

CANDIDATE:

{candidate_to_text(candidate)}

INTERNSHIP:

{job_to_text(selected_job)}

SKILL GAP ANALYSIS:

{skill_gap}

Provide a factual decision-support summary.

Include:

1. Requirements the candidate appears to meet.
2. Requirements that are partially demonstrated.
3. Missing required skills.
4. Missing preferred skills.
5. Relevant projects or education.
6. Areas the candidate could improve.
7. Questions the candidate may want to consider.

Do not tell the candidate whether they should
or should not apply.

Do not rank the internship.

Let the candidate make the final decision.
"""

            llm_response = client.chat.completions.create(

                model=LLM_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You provide neutral application "
                            "decision support."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2
            )

            response = (
                llm_response
                .choices[0]
                .message
                .content
            )

    # ======================================================
    # COMPARE JOBS
    # ======================================================

    elif intent == "compare_jobs":

        # Try to extract two JOB IDs from the message.

        import re

        job_ids = re.findall(
            r"\bJOB\d+\b",
            user_message.upper()
        )

        if len(job_ids) >= 2:

            job1 = get_job_by_id(
                job_ids[0]
            )

            job2 = get_job_by_id(
                job_ids[1]
            )

            if job1 and job2:

                response = compare_jobs(
                    candidate,
                    job1,
                    job2
                )

            else:

                response = (
                    "I could not find both job IDs "
                    "in the current dataset."
                )

        else:

            response = (
                "Please provide two job IDs to compare. "
                "For example: Compare JOB001 and JOB002."
            )

    # ======================================================
    # GENERAL
    # ======================================================

    else:

        response = generate_general_response(
            candidate,
            user_message,
            memory,
            selected_job
        )

    # ------------------------------------------------------
    # Store assistant response
    # ------------------------------------------------------

    memory.add_assistant_message(
        response
    )

    # ------------------------------------------------------
    # Return result
    # ------------------------------------------------------

    return {
        "response": response,
        "intent": intent,
        "selected_job_id": memory.selected_job_id,
        "memory": memory
    }


# ==========================================================
# SELECT JOB
# ==========================================================

def select_job(
    memory,
    job_id
):

    """
    Select an internship for the current conversation.
    """

    job = get_job_by_id(
        job_id
    )

    if job is None:

        return False

    memory.set_selected_job(
        job
    )

    return True