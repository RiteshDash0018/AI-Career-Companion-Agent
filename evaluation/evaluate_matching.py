import sys
import os
<<<<<<< HEAD
=======
import json

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------
>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
<<<<<<< HEAD
=======


# --------------------------------------------------
# Project imports
# --------------------------------------------------

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from rag.query_builder import candidate_to_query
from rag.vector_store import search_jobs
<<<<<<< HEAD


def evaluate_student(name, candidate, expected_keywords):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    # Convert candidate profile into search query
    query = candidate_to_query(candidate)
=======
from agents.job_matching_agent import match_candidate_to_jobs

from evaluation.metrics import (
    print_metrics
)


# --------------------------------------------------
# Count total relevant jobs
# --------------------------------------------------

def count_total_relevant_jobs(expected_keywords):
    """
    Count the total number of relevant jobs
    in the complete dataset.

    Relevance is determined using job-title
    keywords defined for each sample student.
    """

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        jobs = json.load(file)

    total_relevant = 0

    for job in jobs:

        title = job.get(
            "job_title",
            ""
        ).lower()

        if any(
            keyword.lower() in title
            for keyword in expected_keywords
        ):
            total_relevant += 1

    return total_relevant


# --------------------------------------------------
# Evaluate one student
# --------------------------------------------------

def evaluate_student(
    name,
    candidate,
    expected_keywords,
    expected_titles
):

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    # --------------------------------------------------
    # 1. Candidate Query
    # --------------------------------------------------

    query = candidate_to_query(
        candidate
    )
>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444

    print("\nSearch Query:")
    print(query)

<<<<<<< HEAD
    # Search ChromaDB
=======
    # --------------------------------------------------
    # 2. RAG Retrieval
    # --------------------------------------------------

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
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
<<<<<<< HEAD
            f"{index}. {title} - {company}"
        )

        # Check whether the retrieved job
        # contains any expected keyword
=======
            f"{index}. "
            f"{title} - "
            f"{company}"
        )

        # ----------------------------------------------
        # Check retrieval relevance
        # ----------------------------------------------

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
        title_lower = title.lower()

        if any(
            keyword.lower() in title_lower
            for keyword in expected_keywords
        ):
<<<<<<< HEAD
            relevant_count += 1

    accuracy = (
        relevant_count / len(metadatas) * 100
        if metadatas
=======

            relevant_count += 1

    # --------------------------------------------------
    # 3. Retrieval Relevance
    # --------------------------------------------------

    retrieved_count = len(
        metadatas
    )

    retrieval_relevance = (
        relevant_count
        / retrieved_count
        * 100
        if retrieved_count
>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
        else 0
    )

    print(
        f"\nRelevant Results: "
<<<<<<< HEAD
        f"{relevant_count}/{len(metadatas)}"
=======
        f"{relevant_count}/"
        f"{retrieved_count}"
>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
    )

    print(
        f"Retrieval Relevance: "
<<<<<<< HEAD
        f"{accuracy:.2f}%"
    )


# --------------------------------------------------
# Student A — AI / ML
# --------------------------------------------------

student_a = CandidateProfile(
=======
        f"{retrieval_relevance:.2f}%"
    )

    # --------------------------------------------------
    # 4. Precision@5 and Recall@5
    # --------------------------------------------------

    total_relevant_jobs = (
        count_total_relevant_jobs(
            expected_keywords
        )
    )

    print_metrics(
        relevant_results=relevant_count,
        k=5,
        total_relevant_jobs=total_relevant_jobs
    )

    print(
        f"Total Relevant Jobs in Dataset: "
        f"{total_relevant_jobs}"
    )

    # --------------------------------------------------
    # 5. Matching Agent
    # --------------------------------------------------

    print("\nMatching Agent Results:")
    print("-----------------------")

    matches = match_candidate_to_jobs(
        candidate,
        top_k=5
    )

    if not matches:

        print(
            "No matches returned."
        )

        return {
            "student": name,
            "retrieval_relevance": retrieval_relevance,
            "relevant_count": relevant_count,
            "retrieved_count": retrieved_count,
            "precision": 0.0,
            "recall": 0.0,
            "score_consistency": False,
            "skill_accuracy": 0.0,
            "reasoning_quality": 0.0,
            "manual_comparison": False
        }

    # --------------------------------------------------
    # 6. Ranked Matching Results
    # --------------------------------------------------

    print("\nRanked Jobs:")
    print("------------")

    for index, match in enumerate(
        matches,
        start=1
    ):

        print(
            f"{index}. "
            f"{match['title']} - "
            f"{match['company']} - "
            f"{match['compatibility_score']}%"
        )

    # --------------------------------------------------
    # 7. Match Score Consistency
    # --------------------------------------------------

    scores = [
        match["compatibility_score"]
        for match in matches
    ]

    scores_sorted = (
        scores
        == sorted(
            scores,
            reverse=True
        )
    )

    print(
        "\nMatch Score Consistency: "
        + (
            "PASS"
            if scores_sorted
            else "FAIL"
        )
    )

    # --------------------------------------------------
    # 8. Skill Matching Accuracy
    # --------------------------------------------------

    best_match = matches[0]

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        jobs = json.load(file)

    job_map = {
        job["job_id"]: job
        for job in jobs
    }

    best_job = job_map.get(
        best_match["job_id"]
    )

    skill_accuracy = 0.0

    if best_job:

        required_skills = {
            str(skill).lower().strip()
            for skill in best_job.get(
                "required_skills",
                []
            )
            if skill
        }

        candidate_skills = {
            str(skill).lower().strip()
            for skill in candidate.skills
            if skill
        }

        matched_skills = (
            candidate_skills
            .intersection(
                required_skills
            )
        )

        skill_accuracy = (
            len(matched_skills)
            / len(required_skills)
            * 100
            if required_skills
            else 0
        )

        print(
            "\nSkill Matching Evaluation:"
        )

        print(
            "Candidate Skills:"
        )

        print(
            ", ".join(
                candidate.skills
            )
        )

        print(
            "\nMatched Required Skills:"
        )

        if matched_skills:

            print(
                ", ".join(
                    sorted(
                        matched_skills
                    )
                )
            )

        else:

            print("None")

        print(
            f"\nSkill Matching Accuracy: "
            f"{skill_accuracy:.2f}%"
        )

    # --------------------------------------------------
    # 9. Reasoning Quality
    # --------------------------------------------------

    analysis = best_match.get(
        "analysis",
        ""
    )

    reasoning_sections = [
        "Matching Skills",
        "Missing Skills",
        "Qualification",
        "Responsibilities",
        "Reason",
        "Recommendation"
    ]

    explanation_sections_found = 0

    for section in reasoning_sections:

        if (
            section.lower()
            in analysis.lower()
        ):

            explanation_sections_found += 1

    reasoning_quality = (
        explanation_sections_found
        / len(reasoning_sections)
        * 100
    )

    print(
        "\nReasoning / Explanation Evaluation:"
    )

    print(
        f"Required sections found: "
        f"{explanation_sections_found}/"
        f"{len(reasoning_sections)}"
    )

    print(
        f"Reasoning Quality Score: "
        f"{reasoning_quality:.2f}%"
    )

    print(
        "\nAI Explanation:"
    )

    print(
        analysis
    )

    # --------------------------------------------------
    # 10. Manual Expected Result Comparison
    # --------------------------------------------------

    best_title = (
        best_match["title"]
        .lower()
    )

    expected_match = any(
        expected_title.lower()
        in best_title
        or best_title
        in expected_title.lower()
        for expected_title
        in expected_titles
    )

    print(
        "\nManual Expected Result Comparison:"
    )

    print(
        "Expected Job Category: "
        + ", ".join(
            expected_titles
        )
    )

    print(
        "AI Top Recommendation: "
        + best_match["title"]
    )

    print(
        "Manual Comparison: "
        + (
            "PASS"
            if expected_match
            else "CHECK"
        )
    )

    # --------------------------------------------------
    # Return evaluation results
    # --------------------------------------------------

    precision = (
        relevant_count / 5
        if 5 > 0
        else 0
    )

    recall = (
        relevant_count
        / total_relevant_jobs
        if total_relevant_jobs > 0
        else 0
    )

    return {
        "student": name,
        "retrieval_relevance": retrieval_relevance,
        "relevant_count": relevant_count,
        "retrieved_count": retrieved_count,
        "precision": precision,
        "recall": recall,
        "score_consistency": scores_sorted,
        "skill_accuracy": skill_accuracy,
        "reasoning_quality": reasoning_quality,
        "manual_comparison": expected_match
    }


# ==================================================
# STUDENT A — AI / ML
# ==================================================

student_a = CandidateProfile(

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
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


<<<<<<< HEAD
# --------------------------------------------------
# Student B — Web Development
# --------------------------------------------------

student_b = CandidateProfile(
=======
# ==================================================
# STUDENT B — WEB DEVELOPMENT
# ==================================================

student_b = CandidateProfile(

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
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


<<<<<<< HEAD
# --------------------------------------------------
# Student C — Data Science
# --------------------------------------------------

student_c = CandidateProfile(
=======
# ==================================================
# STUDENT C — DATA SCIENCE
# ==================================================

student_c = CandidateProfile(

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
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


<<<<<<< HEAD
# --------------------------------------------------
# Student D — Cybersecurity
# --------------------------------------------------

student_d = CandidateProfile(
=======
# ==================================================
# STUDENT D — CYBERSECURITY
# ==================================================

student_d = CandidateProfile(

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
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


<<<<<<< HEAD
# --------------------------------------------------
# Student E — Cloud / DevOps
# --------------------------------------------------

student_e = CandidateProfile(
=======
# ==================================================
# STUDENT E — CLOUD / DEVOPS
# ==================================================

student_e = CandidateProfile(

>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
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


<<<<<<< HEAD
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
=======
# ==================================================
# RUN ALL EVALUATIONS
# ==================================================

results = []


results.append(
    evaluate_student(
        "Student A - AI / ML",
        student_a,
        [
            "Machine Learning",
            "AI",
            "Artificial Intelligence"
        ],
        [
            "Machine Learning Intern"
        ]
    )
)


results.append(
    evaluate_student(
        "Student B - Web Development",
        student_b,
        [
            "Web",
            "Frontend",
            "Backend",
            "Full Stack"
        ],
        [
            "Frontend",
            "Web",
            "Full Stack"
        ]
    )
)


results.append(
    evaluate_student(
        "Student C - Data Science",
        student_c,
        [
            "Data Science",
            "Data Analyst",
            "Data"
        ],
        [
            "Data Science",
            "Data Analyst",
            "Data"
        ]
    )
)


results.append(
    evaluate_student(
        "Student D - Cybersecurity",
        student_d,
        [
            "Cybersecurity",
            "Security"
        ],
        [
            "Cybersecurity",
            "Security"
        ]
    )
)


results.append(
    evaluate_student(
        "Student E - Cloud / DevOps",
        student_e,
        [
            "Cloud",
            "DevOps"
        ],
        [
            "DevOps",
            "Cloud"
        ]
    )
)


# ==================================================
# FINAL M2.4 SUMMARY
# ==================================================

print("\n\n")
print("=" * 80)
print("FINAL M2.4 EVALUATION SUMMARY")
print("=" * 80)

if results:

    average_retrieval = (
        sum(
            result["retrieval_relevance"]
            for result in results
        )
        / len(results)
    )

    average_precision = (
        sum(
            result["precision"]
            for result in results
        )
        / len(results)
    )

    average_recall = (
        sum(
            result["recall"]
            for result in results
        )
        / len(results)
    )

    average_skill_accuracy = (
        sum(
            result["skill_accuracy"]
            for result in results
        )
        / len(results)
    )

    average_reasoning = (
        sum(
            result["reasoning_quality"]
            for result in results
        )
        / len(results)
    )

    score_consistency_count = sum(
        result["score_consistency"]
        for result in results
    )

    manual_pass_count = sum(
        result["manual_comparison"]
        for result in results
    )

    print(
        f"\nAverage Retrieval Relevance: "
        f"{average_retrieval:.2f}%"
    )

    print(
        f"Average Precision@5: "
        f"{average_precision * 100:.2f}%"
    )

    print(
        f"Average Recall@5: "
        f"{average_recall * 100:.2f}%"
    )

    print(
        f"Average Skill Matching Accuracy: "
        f"{average_skill_accuracy:.2f}%"
    )

    print(
        f"Average Reasoning Quality: "
        f"{average_reasoning:.2f}%"
    )

    print(
        f"Score Consistency: "
        f"{score_consistency_count}/"
        f"{len(results)} PASS"
    )

    print(
        f"Manual Comparison: "
        f"{manual_pass_count}/"
        f"{len(results)} PASS"
    )

print("\n" + "=" * 80)
print("M2.4 EVALUATION COMPLETE")
print("=" * 80)
>>>>>>> c8168fafca1fd8db10d45b65c19c268f0c5ec444
