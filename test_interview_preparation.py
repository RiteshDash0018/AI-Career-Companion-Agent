import json

from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from agents.skill_gap_agent import skill_gap_analysis

from agents.interview_preparation_agent import (
    prepare_interview
)


# ==========================================================
# LOAD JOB
# ==========================================================

def load_test_job():

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        jobs = json.load(file)

    return jobs[0]


# ==========================================================
# CREATE TEST CANDIDATE
# ==========================================================

def create_test_candidate():

    return CandidateProfile(

        name="Test Student",

        email="test@example.com",

        phone="9999999999",

        skills=[
            "Python",
            "Machine Learning",
            "SQL",
            "Pandas",
            "NumPy",
            "TensorFlow"
        ],

        education=[
            Education(
                degree="B.Tech Computer Science",
                institution="SOA University",
                year="2026"
            )
        ],

        projects=[
            Project(
                name="Machine Learning Project",

                description=(
                    "Developed a machine learning "
                    "prediction system using Python "
                    "and TensorFlow."
                ),

                technologies=[
                    "Python",
                    "Pandas",
                    "NumPy",
                    "TensorFlow"
                ]
            )
        ],

        certifications=[
            "Machine Learning Certification"
        ],

        career_interests=[
            "Machine Learning",
            "Artificial Intelligence"
        ]
    )


# ==========================================================
# MAIN TEST
# ==========================================================

def main():

    print("\n" + "=" * 70)
    print("M3.3 - INTERVIEW PREPARATION AGENT TEST")
    print("=" * 70)

    # ------------------------------------------------------
    # Candidate
    # ------------------------------------------------------

    candidate = create_test_candidate()

    print("\nCandidate:")
    print(candidate.name)

    # ------------------------------------------------------
    # Job
    # ------------------------------------------------------

    job = load_test_job()

    print("\nSelected Job:")
    print(job["job_title"])

    print("\nCompany:")
    print(job["company"])

    # ------------------------------------------------------
    # Skill Gap Analysis
    # ------------------------------------------------------

    print("\nRunning skill gap analysis...")

    skill_gap = skill_gap_analysis(
        candidate,
        job
    )

    print("\nSkill gap analysis generated successfully.")

    # ------------------------------------------------------
    # Interview Preparation
    # ------------------------------------------------------

    print("\nGenerating interview preparation...")

    result = prepare_interview(
        candidate,
        job,
        skill_gap
    )

    # ------------------------------------------------------
    # Interview Questions
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("INTERVIEW QUESTIONS")
    print("=" * 70)

    print(result["interview_questions"])

    # ------------------------------------------------------
    # Revision Topics
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("REVISION TOPICS")
    print("=" * 70)

    print(result["revision_topics"])

    # ------------------------------------------------------
    # Basic validation
    # ------------------------------------------------------

    if result["interview_questions"]:
        print("\nInterview Question Generation: PASS")
    else:
        print("\nInterview Question Generation: FAIL")

    if result["revision_topics"]:
        print("Revision Topic Generation: PASS")
    else:
        print("Revision Topic Generation: FAIL")

    print("\n" + "=" * 70)
    print("M3.3 BASIC TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()