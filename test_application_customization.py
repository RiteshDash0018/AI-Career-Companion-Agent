import json

from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from agents.application_customization_agent import (
    customize_application
)


# ============================================================
# LOAD JOB
# ============================================================

def load_test_job():

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        jobs = json.load(file)

    return jobs[0]


# ============================================================
# CREATE TEST CANDIDATE
# ============================================================

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


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("\n" + "=" * 60)

    print(
        "M3.2 - RESUME & COVER LETTER "
        "CUSTOMIZATION TEST"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # Candidate
    # --------------------------------------------------------

    candidate = create_test_candidate()

    print("\nCandidate:")
    print(candidate.name)

    # --------------------------------------------------------
    # Job
    # --------------------------------------------------------

    job = load_test_job()

    print("\nSelected Job:")
    print(job["job_title"])

    print("\nCompany:")
    print(job["company"])

    # --------------------------------------------------------
    # Generate application
    # --------------------------------------------------------

    print(
        "\nGenerating customized resume "
        "and cover letter..."
    )

    result = customize_application(
        candidate,
        job
    )

    # --------------------------------------------------------
    # Resume
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print("CUSTOMIZED RESUME")

    print("=" * 60)

    print(
        result["resume"]
    )

    # --------------------------------------------------------
    # Cover letter
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print("CUSTOMIZED COVER LETTER")

    print("=" * 60)

    print(
        result["cover_letter"]
    )

    # --------------------------------------------------------
    # Test status
    # --------------------------------------------------------

    if result["resume"]:

        print(
            "\nResume Generation: PASS"
        )

    else:

        print(
            "\nResume Generation: FAIL"
        )

    if result["cover_letter"]:

        print(
            "Cover Letter Generation: PASS"
        )

    else:

        print(
            "Cover Letter Generation: FAIL"
        )

    print("\n" + "=" * 60)

    print(
        "M3.2 BASIC TEST COMPLETE"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()