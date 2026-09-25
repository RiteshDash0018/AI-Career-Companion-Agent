import json

from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from agents.skill_gap_agent import (
    skill_gap_analysis
)


# ============================================================
# LOAD A REAL JOB FROM jobs.json
# ============================================================

def load_test_job():

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        jobs = json.load(file)

    # Use JOB001
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
    print("M3.1 - SKILL GAP ANALYSIS TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # Create candidate
    # --------------------------------------------------------

    candidate = create_test_candidate()

    print("\nCandidate:")
    print(candidate.name)

    print("\nCandidate Skills:")
    print(", ".join(candidate.skills))

    # --------------------------------------------------------
    # Load job
    # --------------------------------------------------------

    job = load_test_job()

    print("\nSelected Job:")
    print(job["job_title"])

    print("\nCompany:")
    print(job["company"])

    # --------------------------------------------------------
    # Run Skill Gap Agent
    # --------------------------------------------------------

    print("\nRunning Skill Gap Analysis...")

    result = skill_gap_analysis(
        candidate,
        job
    )

    analysis = result["analysis"]

    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    print("\n" + "-" * 60)
    print("REQUIRED SKILLS")
    print("-" * 60)

    print(
        "Matched Required Skills:"
    )

    print(
        analysis[
            "matched_required_skills"
        ]
    )

    print(
        "\nCritical/Missing Required Skills:"
    )

    print(
        analysis[
            "critical_missing_skills"
        ]
    )

    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("PARTIALLY DEMONSTRATED SKILLS")
    print("-" * 60)

    partial_skills = analysis[
        "partially_demonstrated_skills"
    ]

    if partial_skills:

        for item in partial_skills:

            print(
                f"- {item['skill']}"
            )

            print(
                f"  Evidence: "
                f"{', '.join(item['evidence'])}"
            )

    else:

        print(
            "None identified."
        )

    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("PREFERRED SKILLS")
    print("-" * 60)

    print(
        "Matched Preferred Skills:"
    )

    print(
        analysis[
            "matched_preferred_skills"
        ]
    )

    print(
        "\nPreferred Skill Gaps:"
    )

    print(
        analysis[
            "preferred_skill_gaps"
        ]
    )

    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("EDUCATION")
    print("-" * 60)

    print(
        analysis[
            "education_gap"
        ]
    )

    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("EXPERIENCE")
    print("-" * 60)

    print(
        analysis[
            "experience_gap"
        ]
    )

    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("QUALIFICATION")
    print("-" * 60)

    print(
        analysis[
            "qualification_gap"
        ]
    )

    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("PROJECT EVIDENCE")
    print("-" * 60)

    print(
        analysis[
            "project_evidence"
        ]
    )

    # ========================================================
    # LLM EXPLANATION
    # ========================================================

    print("\n" + "=" * 60)
    print("AI-GENERATED SKILL GAP ANALYSIS")
    print("=" * 60)

    print(
        result["explanation"]
    )

    # ========================================================
    # TEST COMPLETE
    # ========================================================

    print("\n" + "=" * 60)
    print("M3.1 TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()