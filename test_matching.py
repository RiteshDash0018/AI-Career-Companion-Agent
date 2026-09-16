from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from agents.job_matching_agent import (
    match_candidate_to_jobs
)


# --------------------------------------------------
# Create candidate profile
# --------------------------------------------------

candidate = CandidateProfile(

    skills=[
        "Python",
        "Machine Learning",
        "SQL",
        "Pandas"
    ],

    education=[
        Education(
            degree="B.Tech Computer Science",
            institution="Example University",
            year="2026"
        )
    ],

    projects=[
        Project(
            name="AI Career Companion",
            description=(
                "An AI system for internship "
                "matching and career recommendations"
            ),
            technologies=[
                "Python",
                "Machine Learning",
                "LangChain"
            ]
        ),

        Project(
            name="Commodity Price Prediction",
            description=(
                "A machine learning project "
                "for predicting commodity prices"
            ),
            technologies=[
                "Python",
                "Pandas",
                "Scikit-learn"
            ]
        )
    ],

    certifications=[
        "Python Certification"
    ],

    career_interests=[
        "Artificial Intelligence",
        "Machine Learning"
    ]
)


# --------------------------------------------------
# Run matching agent
# --------------------------------------------------

matches = match_candidate_to_jobs(
    candidate,
    top_k=5
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n")
print("=" * 60)
print("TOP INTERNSHIP RECOMMENDATIONS")
print("=" * 60)


for index, match in enumerate(matches, start=1):

    print(f"\n{index}. {match['title']}")

    print(
        f"Company: {match['company']}"
    )

    print(
        f"Location: {match['location']}"
    )

    print(
    f"\nCompatibility Score: "
    f"{match['compatibility_score']}%"
    )

    print("\nAI Analysis:")
    print(match["analysis"])

    print("-" * 60)