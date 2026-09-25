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
# CREATE TEST CANDIDATE
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
# CREATE CONVERSATION MEMORY
# ============================================================

memory = ConversationMemory()


# ============================================================
# LOAD TEST JOB
# ============================================================

job = get_job_by_id("JOB001")


if job is None:

    print(
        "ERROR: JOB001 was not found in data/jobs.json"
    )

    exit()


# ============================================================
# SELECT JOB
# ============================================================

selected = select_job(
    memory,
    "JOB001"
)


if not selected:

    print(
        "ERROR: Could not select JOB001"
    )

    exit()


# ============================================================
# DISPLAY TEST INFORMATION
# ============================================================

print(
    "\n=================================================="
)

print(
    "M3.4 - CONVERSATIONAL CAREER ASSISTANT TEST"
)

print(
    "=================================================="
)

print(
    f"Candidate: {candidate.name}"
)

print(
    f"Selected Job: "
    f"{job.get('job_title', '')}"
)

print(
    f"Company: "
    f"{job.get('company', '')}"
)

print(
    f"Job ID: "
    f"{job.get('job_id', '')}"
)


# ============================================================
# TEST 1 - JOB RECOMMENDATION
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 1: JOB RECOMMENDATION"
)

print(
    "--------------------------------------------------"
)

message = (
    "Recommend suitable internships for me."
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 2 - JOB REQUIREMENTS
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 2: JOB REQUIREMENTS"
)

print(
    "--------------------------------------------------"
)

message = (
    "What are the requirements for this internship?"
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 3 - SKILL GAP
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 3: SKILL GAP ANALYSIS"
)

print(
    "--------------------------------------------------"
)

message = (
    "What are my skill gaps for this role?"
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 4 - RESUME CUSTOMIZATION
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 4: RESUME CUSTOMIZATION"
)

print(
    "--------------------------------------------------"
)

message = (
    "How should I customize my resume "
    "for this internship?"
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 5 - COVER LETTER
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 5: COVER LETTER"
)

print(
    "--------------------------------------------------"
)

message = (
    "Create a cover letter for this internship."
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 6 - INTERVIEW PREPARATION
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 6: INTERVIEW PREPARATION"
)

print(
    "--------------------------------------------------"
)

message = (
    "How should I prepare for the interview?"
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 7 - GENERAL CAREER QUESTION
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 7: GENERAL CAREER QUESTION"
)

print(
    "--------------------------------------------------"
)

message = (
    "Which of my skills are most relevant "
    "to this internship?"
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# TEST 8 - COMPARE TWO JOBS
# ============================================================

print(
    "\n--------------------------------------------------"
)

print(
    "TEST 8: COMPARE INTERNSHIPS"
)

print(
    "--------------------------------------------------"
)

message = (
    "Compare JOB001 and JOB002."
)

result = chat(
    candidate,
    message,
    memory
)

print(
    result["response"]
)

print(
    "\nDetected Intent:",
    result["intent"]
)


# ============================================================
# VALIDATION
# ============================================================

print(
    "\n=================================================="
)

print(
    "M3.4 VALIDATION"
)

print(
    "=================================================="
)


# ------------------------------------------------------------
# Check response
# ------------------------------------------------------------

if result["response"]:

    print(
        "PASS: Assistant returned a response."
    )

else:

    print(
        "FAIL: Assistant returned an empty response."
    )


# ------------------------------------------------------------
# Check intent
# ------------------------------------------------------------

if result["intent"]:

    print(
        "PASS: Intent detection is working."
    )

else:

    print(
        "FAIL: Intent detection failed."
    )


# ------------------------------------------------------------
# Check selected job
# ------------------------------------------------------------

if memory.selected_job_id == "JOB001":

    print(
        "PASS: Selected job context retained."
    )

else:

    print(
        "FAIL: Selected job context was lost."
    )


# ------------------------------------------------------------
# Check conversation memory
# ------------------------------------------------------------

if len(memory.messages) >= 16:

    print(
        "PASS: Conversation memory retained."
    )

else:

    print(
        "FAIL: Conversation memory test failed."
    )


# ------------------------------------------------------------
# Check selected job object
# ------------------------------------------------------------

if memory.selected_job is not None:

    print(
        "PASS: Selected internship information retained."
    )

else:

    print(
        "FAIL: Selected internship information missing."
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print(
    "\n=================================================="
)

print(
    "M3.4 BASIC TEST COMPLETE"
)

print(
    "=================================================="
)