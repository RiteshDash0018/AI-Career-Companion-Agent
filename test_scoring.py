from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from agents.scoring import calculate_compatibility_score


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
            description="AI based internship matching system",
            technologies=[
                "Python",
                "Machine Learning",
                "LangChain"
            ]
        )
    ]
)


job = {
    "job_id": "JOB001",
    "title": "Machine Learning Intern",
    "required_skills": [
        "Python",
        "Machine Learning",
        "SQL"
    ],
    "preferred_skills": [
        "Pandas",
        "TensorFlow"
    ],
    "education": "B.Tech/B.E. in Computer Science",
    "experience": "Fresher / 0-1 years"
}


score = calculate_compatibility_score(
    candidate,
    job
)

print("Compatibility Score:", score, "%")