import json

from models.candidate import (
    CandidateProfile,
    Education,
    Project
)

from agents.career_assistant import (
    ConversationMemory,
    chat,
    get_job_by_id,
    select_job
)


# ============================================================
# M3 FINAL EVALUATION
# ============================================================

print("\n==================================================")
print("MILESTONE 3 - FINAL EVALUATION")
print("==================================================")


# ============================================================
# TEST CANDIDATE
# ============================================================

candidate = CandidateProfile(

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
# LOAD JOB
# ============================================================

job = get_job_by_id("JOB001")


if job is None:

    print("FAIL: JOB001 not found.")

    exit()


print(
    f"\nCandidate: {candidate.name}"
)

print(
    f"Selected Job: "
    f"{job.get('job_title', '')}"
)

print(
    f"Company: "
    f"{job.get('company', '')}"
)


# ============================================================
# CREATE MEMORY
# ============================================================

memory = ConversationMemory()


selected = select_job(
    memory,
    "JOB001"
)


if selected:

    print(
        "PASS: Job selection successful."
    )

else:

    print(
        "FAIL: Job selection failed."
    )


# ============================================================
# EVALUATION RESULTS
# ============================================================

results = {}


# ============================================================
# M3.1 - SKILL GAP ANALYSIS
# ============================================================

print("\n--------------------------------------------------")
print("M3.1 - SKILL GAP ANALYSIS")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "What are my skill gaps for this role?",
        memory
    )

    if (
        result["response"]
        and result["intent"] == "skill_gap"
    ):

        results["M3.1"] = "PASS"

        print(
            "PASS: Skill Gap Analysis Agent integrated."
        )

    else:

        results["M3.1"] = "FAIL"

        print(
            "FAIL: Skill Gap Analysis test failed."
        )

except Exception as error:

    results["M3.1"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.2 - RESUME CUSTOMIZATION
# ============================================================

print("\n--------------------------------------------------")
print("M3.2 - RESUME CUSTOMIZATION")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "Customize my resume for this internship.",
        memory
    )

    if (
        result["response"]
        and result["intent"] == "resume"
    ):

        results["M3.2 Resume"] = "PASS"

        print(
            "PASS: Resume customization integrated."
        )

    else:

        results["M3.2 Resume"] = "FAIL"

        print(
            "FAIL: Resume customization test failed."
        )

except Exception as error:

    results["M3.2 Resume"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.2 - COVER LETTER
# ============================================================

print("\n--------------------------------------------------")
print("M3.2 - COVER LETTER")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "Create a cover letter for this internship.",
        memory
    )

    if (
        result["response"]
        and result["intent"] == "cover_letter"
    ):

        results["M3.2 Cover Letter"] = "PASS"

        print(
            "PASS: Cover letter generation integrated."
        )

    else:

        results["M3.2 Cover Letter"] = "FAIL"

        print(
            "FAIL: Cover letter test failed."
        )

except Exception as error:

    results["M3.2 Cover Letter"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.3 - INTERVIEW PREPARATION
# ============================================================

print("\n--------------------------------------------------")
print("M3.3 - INTERVIEW PREPARATION")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "How should I prepare for the interview?",
        memory
    )

    if (
        result["response"]
        and result["intent"] == "interview"
    ):

        results["M3.3"] = "PASS"

        print(
            "PASS: Interview Preparation Agent integrated."
        )

    else:

        results["M3.3"] = "FAIL"

        print(
            "FAIL: Interview preparation test failed."
        )

except Exception as error:

    results["M3.3"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.4 - JOB RECOMMENDATION
# ============================================================

print("\n--------------------------------------------------")
print("M3.4 - JOB RECOMMENDATION")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "Recommend suitable internships for me.",
        memory
    )

    if (
        result["response"]
        and result["intent"]
        == "job_recommendation"
    ):

        results["M3.4 Recommendations"] = "PASS"

        print(
            "PASS: Job recommendation integration works."
        )

    else:

        results["M3.4 Recommendations"] = "FAIL"

        print(
            "FAIL: Job recommendation failed."
        )

except Exception as error:

    results["M3.4 Recommendations"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.4 - JOB REQUIREMENTS
# ============================================================

print("\n--------------------------------------------------")
print("M3.4 - JOB REQUIREMENTS")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "What are the requirements for this internship?",
        memory
    )

    if (
        result["response"]
        and result["intent"]
        == "job_requirements"
    ):

        results["M3.4 Requirements"] = "PASS"

        print(
            "PASS: Job requirements response works."
        )

    else:

        results["M3.4 Requirements"] = "FAIL"

        print(
            "FAIL: Job requirements test failed."
        )

except Exception as error:

    results["M3.4 Requirements"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.4 - GENERAL CONVERSATION
# ============================================================

print("\n--------------------------------------------------")
print("M3.4 - GENERAL CONVERSATION")
print("--------------------------------------------------")

try:

    result = chat(
        candidate,
        "Which of my skills are most relevant to this internship?",
        memory
    )

    if (
        result["response"]
        and result["intent"] == "general"
    ):

        results["M3.4 Conversation"] = "PASS"

        print(
            "PASS: General conversational response works."
        )

    else:

        results["M3.4 Conversation"] = "FAIL"

        print(
            "FAIL: General conversation test failed."
        )

except Exception as error:

    results["M3.4 Conversation"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# M3.4 - CONTEXT RETENTION
# ============================================================

print("\n--------------------------------------------------")
print("M3.4 - CONTEXT RETENTION")
print("--------------------------------------------------")

try:

    if (
        memory.selected_job_id == "JOB001"
        and len(memory.messages) > 0
    ):

        results["M3.4 Context"] = "PASS"

        print(
            "PASS: Conversation context retained."
        )

    else:

        results["M3.4 Context"] = "FAIL"

        print(
            "FAIL: Conversation context not retained."
        )

except Exception as error:

    results["M3.4 Context"] = "FAIL"

    print(
        "FAIL:",
        error
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n==================================================")
print("M3 FINAL RESULTS")
print("==================================================")


passed = 0
failed = 0


for test_name, status in results.items():

    print(
        f"{test_name}: {status}"
    )

    if status == "PASS":

        passed += 1

    else:

        failed += 1


total = passed + failed


print("\n--------------------------------------------------")

print(
    f"Tests Passed: {passed}/{total}"
)

print(
    f"Tests Failed: {failed}/{total}"
)


if failed == 0:

    print(
        "\nMILESTONE 3 FINAL EVALUATION: PASS"
    )

    print(
        "All implemented M3 components passed."
    )

else:

    print(
        "\nMILESTONE 3 FINAL EVALUATION: NEEDS REVIEW"
    )

    print(
        "Some components require additional testing."
    )


print("==================================================")