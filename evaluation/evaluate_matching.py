import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from rag.query_builder import candidate_to_query
from rag.vector_store import search_jobs


def evaluate_student(name, candidate, expected_keywords):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    # Convert candidate profile into search query
    query = candidate_to_query(candidate)

    print("\nSearch Query:")
    print(query)

    # Search ChromaDB
    results = search_jobs(
        query,
        top_k=5
    )

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    print("\nTop 5 Retrieved Jobs:")
    print("---------------------")

    relevant_count = 0

    for index, metadata in enumerate(
        metadatas,
        start=1
    ):

        title = metadata.get(
            "title",
            ""
        )

        company = metadata.get(
            "company",
            ""
        )

        print(
            f"{index}. {title} - {company}"
        )

        # Check whether the retrieved job
        # contains any expected keyword
        title_lower = title.lower()

        if any(
            keyword.lower() in title_lower
            for keyword in expected_keywords
        ):
            relevant_count += 1

    accuracy = (
        relevant_count / len(metadatas) * 100
        if metadatas
        else 0
    )

    print(
        f"\nRelevant Results: "
        f"{relevant_count}/{len(metadatas)}"
    )

    print(
        f"Retrieval Relevance: "
        f"{accuracy:.2f}%"
    )


# --------------------------------------------------
# Student A — AI / ML
# --------------------------------------------------

student_a = CandidateProfile(
    skills=[
        "Python",
        "Machine Learning",
        "SQL",
        "Pandas",
        "Scikit-learn"
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
            name="Machine Learning Project",
            description="Built predictive machine learning models",
            technologies=[
                "Python",
                "Machine Learning",
                "Scikit-learn"
            ]
        )
    ],

    career_interests=[
        "Artificial Intelligence",
        "Machine Learning"
    ]
)


# --------------------------------------------------
# Student B — Web Development
# --------------------------------------------------

student_b = CandidateProfile(
    skills=[
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js"
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
            name="E-Commerce Website",
            description="Built a responsive full-stack web application",
            technologies=[
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Node.js"
            ]
        )
    ],

    career_interests=[
        "Web Development",
        "Frontend Development",
        "Backend Development"
    ]
)


# --------------------------------------------------
# Student C — Data Science
# --------------------------------------------------

student_c = CandidateProfile(
    skills=[
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "Data Analysis"
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
            name="Sales Data Analysis",
            description="Analyzed business data and created visualizations",
            technologies=[
                "Python",
                "Pandas",
                "NumPy",
                "SQL"
            ]
        )
    ],

    career_interests=[
        "Data Science",
        "Data Analytics"
    ]
)


# --------------------------------------------------
# Student D — Cybersecurity
# --------------------------------------------------

student_d = CandidateProfile(
    skills=[
        "Cybersecurity",
        "Network Security",
        "Linux",
        "Python",
        "Ethical Hacking"
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
            name="Network Security Monitor",
            description="Built a system to monitor network activity",
            technologies=[
                "Python",
                "Linux",
                "Network Security"
            ]
        )
    ],

    career_interests=[
        "Cybersecurity",
        "Information Security"
    ]
)


# --------------------------------------------------
# Student E — Cloud / DevOps
# --------------------------------------------------

student_e = CandidateProfile(
    skills=[
        "AWS",
        "Docker",
        "Linux",
        "Kubernetes",
        "CI/CD"
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
            name="Cloud Deployment Project",
            description="Deployed an application using cloud infrastructure",
            technologies=[
                "AWS",
                "Docker",
                "Kubernetes"
            ]
        )
    ],

    career_interests=[
        "Cloud Computing",
        "DevOps"
    ]
)


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

evaluate_student(
    "Student A - AI / ML",
    student_a,
    [
        "Machine Learning",
        "AI",
        "Artificial Intelligence"
    ]
)

evaluate_student(
    "Student B - Web Development",
    student_b,
    [
        "Web",
        "Frontend",
        "Backend",
        "Full Stack"
    ]
)

evaluate_student(
    "Student C - Data Science",
    student_c,
    [
        "Data Science",
        "Data Analyst",
        "Data"
    ]
)

evaluate_student(
    "Student D - Cybersecurity",
    student_d,
    [
        "Cybersecurity",
        "Security"
    ]
)

evaluate_student(
    "Student E - Cloud / DevOps",
    student_e,
    [
        "Cloud",
        "DevOps"
    ]
)