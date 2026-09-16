from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from rag.query_builder import candidate_to_query


candidate = CandidateProfile(
    skills=[
        "Python",
        "Machine Learning",
        "SQL"
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
            description="An AI system for internship matching",
            technologies=[
                "Python",
                "Machine Learning",
                "LangChain"
            ]
        ),

        Project(
            name="Commodity Price Prediction",
            description="A machine learning model for predicting commodity prices",
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


query = candidate_to_query(candidate)

print("Candidate Search Query:")
print("-----------------------")
print(query)