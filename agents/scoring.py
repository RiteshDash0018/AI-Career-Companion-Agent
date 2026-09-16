# ============================================================
# JOB-RESUME COMPATIBILITY SCORING
# ============================================================

import re


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    """
    Convert text into a normalized lowercase form.
    """

    if not text:
        return ""

    text = str(text).lower().strip()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9+#.\- ]", " ", text)

    # Remove extra spaces
    text = " ".join(text.split())

    return text


# ============================================================
# RELATED SKILL GROUPS
# ============================================================

RELATED_SKILLS = {

    "python": {
        "python",
        "python programming",
        "python development"
    },

    "machine learning": {
        "machine learning",
        "ml",
        "machine learning algorithms"
    },

    "deep learning": {
        "deep learning",
        "neural networks",
        "deep neural networks"
    },

    "data science": {
        "data science",
        "data analysis",
        "data analytics"
    },

    "sql": {
        "sql",
        "mysql",
        "postgresql",
        "database"
    },

    "pandas": {
        "pandas",
        "data manipulation"
    },

    "numpy": {
        "numpy",
        "numerical computing"
    },

    "scikit-learn": {
        "scikit-learn",
        "sklearn",
        "machine learning library"
    },

    "tensorflow": {
        "tensorflow",
        "keras"
    },

    "pytorch": {
        "pytorch",
        "torch"
    },

    "javascript": {
        "javascript",
        "js"
    },

    "react": {
        "react",
        "react.js",
        "reactjs"
    },

    "html": {
        "html",
        "html5"
    },

    "css": {
        "css",
        "css3"
    },

    "node.js": {
        "node.js",
        "nodejs",
        "node"
    },

    "frontend": {
        "frontend",
        "front-end",
        "frontend development"
    },

    "web development": {
        "web development",
        "web development technologies"
    },

    "cybersecurity": {
        "cybersecurity",
        "cyber security",
        "information security"
    },

    "network security": {
        "network security",
        "networking",
        "computer networks"
    },

    "ethical hacking": {
        "ethical hacking",
        "penetration testing",
        "pen testing"
    },

    "linux": {
        "linux",
        "unix"
    },

    "aws": {
        "aws",
        "amazon web services"
    },

    "docker": {
        "docker",
        "containerization",
        "containers"
    },

    "kubernetes": {
        "kubernetes",
        "k8s"
    },

    "devops": {
        "devops",
        "dev ops",
        "continuous integration",
        "continuous deployment",
        "ci/cd"
    },

    "git": {
        "git",
        "github",
        "version control"
    },

    "java": {
        "java",
        "java programming"
    },

    "c++": {
        "c++",
        "cpp"
    },

    "c": {
        "c",
        "c programming"
    }
}


# ============================================================
# FIND RELATED SKILL GROUP
# ============================================================

def get_skill_group(skill):
    """
    Find the related skill group for a skill.
    """

    skill = normalize(skill)

    if not skill:
        return None

    for group_name, related_skills in RELATED_SKILLS.items():

        normalized_related = {
            normalize(item)
            for item in related_skills
        }

        if skill in normalized_related:
            return group_name

    return None


# ============================================================
# SKILL COMPARISON
# ============================================================

def skills_are_related(candidate_skill, job_skill):
    """
    Check whether two skills are identical or related.
    """

    candidate_skill = normalize(candidate_skill)
    job_skill = normalize(job_skill)

    if not candidate_skill or not job_skill:
        return False

    # Exact match
    if candidate_skill == job_skill:
        return True

    # Candidate skill contains job skill
    if (
        candidate_skill in job_skill
        or job_skill in candidate_skill
    ):
        return True

    candidate_group = get_skill_group(
        candidate_skill
    )

    job_group = get_skill_group(
        job_skill
    )

    if (
        candidate_group
        and job_group
        and candidate_group == job_group
    ):
        return True

    return False


def skill_match(candidate_skills, job_skills):
    """
    Calculate percentage of job skills matched
    by the candidate.

    Each job skill contributes equally.
    """

    if not job_skills:
        return 0.0

    candidate_skills = [
        normalize(skill)
        for skill in candidate_skills
        if skill
    ]

    job_skills = [
        normalize(skill)
        for skill in job_skills
        if skill
    ]

    if not candidate_skills or not job_skills:
        return 0.0

    matched_count = 0

    for job_skill in job_skills:

        matched = any(
            skills_are_related(
                candidate_skill,
                job_skill
            )
            for candidate_skill in candidate_skills
        )

        if matched:
            matched_count += 1

    return matched_count / len(job_skills)


# ============================================================
# TEXT SIMILARITY
# ============================================================

def text_keyword_match(candidate_text, job_text):
    """
    Calculate simple keyword overlap between
    candidate text and job text.
    """

    candidate_text = normalize(candidate_text)
    job_text = normalize(job_text)

    if not candidate_text or not job_text:
        return 0.0

    candidate_words = set(
        word
        for word in candidate_text.split()
        if len(word) > 2
    )

    job_words = set(
        word
        for word in job_text.split()
        if len(word) > 2
    )

    if not job_words:
        return 0.0

    common_words = candidate_words.intersection(
        job_words
    )

    return len(common_words) / len(job_words)


# ============================================================
# EDUCATION MATCH
# ============================================================

def education_match(candidate, job):
    """
    Compare candidate education with the
    internship education requirements.
    """

    if not candidate.education:
        return 0.0

    job_education = normalize(
        job.get(
            "education_requirements",
            ""
        )
    )

    qualification = normalize(
        job.get(
            "qualification",
            ""
        )
    )

    combined_job_education = (
        job_education + " " + qualification
    )

    if not combined_job_education:
        return 0.0


    # --------------------------------------------------------
    # Degree indicators
    # --------------------------------------------------------

    degree_groups = {

        "btech": {
            "btech",
            "b.tech",
            "b.e",
            "be",
            "bachelor of engineering",
            "bachelor of technology"
        },

        "mtech": {
            "mtech",
            "m.tech",
            "master of technology",
            "master of engineering"
        },

        "bsc": {
            "bsc",
            "b.sc",
            "bachelor of science"
        },

        "msc": {
            "msc",
            "m.sc",
            "master of science"
        },

        "bca": {
            "bca",
            "bachelor of computer applications"
        },

        "mca": {
            "mca",
            "master of computer applications"
        }
    }


    for education in candidate.education:

        candidate_degree = normalize(
            education.degree
        )

        if not candidate_degree:
            continue


        # Exact text match

        if candidate_degree in combined_job_education:

            return 1.0


        # Check degree groups

        for group_name, degrees in degree_groups.items():

            candidate_has_group = any(
                normalize(degree)
                in candidate_degree
                for degree in degrees
            )

            job_has_group = any(
                normalize(degree)
                in combined_job_education
                for degree in degrees
            )

            if candidate_has_group and job_has_group:

                return 1.0


        # Computer science / related field

        computer_science_terms = [
            "computer science",
            "computer engineering",
            "information technology",
            "information science",
            "software engineering"
        ]

        candidate_degree_is_cs = any(
            term in candidate_degree
            for term in computer_science_terms
        )

        job_requires_cs = any(
            term in combined_job_education
            for term in computer_science_terms
        )

        if candidate_degree_is_cs and job_requires_cs:

            return 1.0


    return 0.0


# ============================================================
# EXPERIENCE MATCH
# ============================================================

def experience_match(candidate, job):
    """
    Compare candidate experience with
    internship experience requirements.
    """

    required_experience = normalize(
        job.get(
            "experience_requirements",
            ""
        )
    )


    # No requirement specified

    if not required_experience:

        return 0.5


    # --------------------------------------------------------
    # Internship accepts freshers
    # --------------------------------------------------------

    fresher_terms = [
        "fresher",
        "freshers",
        "0-1",
        "0 1",
        "entry level",
        "entry-level",
        "no experience",
        "students",
        "student"
    ]

    accepts_fresher = any(
        term in required_experience
        for term in fresher_terms
    )


    if accepts_fresher:

        # Candidate has no experience
        if not candidate.experience:

            return 1.0

        # Candidate has experience
        return 1.0


    # --------------------------------------------------------
    # Candidate has experience
    # --------------------------------------------------------

    if candidate.experience:

        return 1.0


    return 0.0


# ============================================================
# PROJECT MATCH
# ============================================================

def project_match(candidate, job):
    """
    Compare candidate projects with internship
    required and preferred skills.

    Project technologies have higher importance
    than general project description keywords.
    """

    if not candidate.projects:

        return 0.0


    # --------------------------------------------------------
    # Candidate project technologies
    # --------------------------------------------------------

    candidate_technologies = []

    candidate_descriptions = []


    for project in candidate.projects:

        for technology in project.technologies:

            if technology:

                candidate_technologies.append(
                    normalize(technology)
                )


        if project.description:

            candidate_descriptions.append(
                normalize(
                    project.description
                )
            )


    # --------------------------------------------------------
    # Job skills
    # --------------------------------------------------------

    required_skills = job.get(
        "required_skills",
        []
    )

    preferred_skills = job.get(
        "preferred_skills",
        []
    )

    all_job_skills = (
        required_skills
        + preferred_skills
    )


    if not all_job_skills:

        return 0.0


    # --------------------------------------------------------
    # Technology match
    # --------------------------------------------------------

    technology_score = skill_match(
        candidate_technologies,
        all_job_skills
    )


    # --------------------------------------------------------
    # Project description match
    # --------------------------------------------------------

    description_text = " ".join(
        candidate_descriptions
    )

    job_text = " ".join(
        [
            normalize(skill)
            for skill in all_job_skills
        ]
    )


    description_score = text_keyword_match(
        description_text,
        job_text
    )


    # --------------------------------------------------------
    # Final project score
    # --------------------------------------------------------

    final_project_score = (
        technology_score * 0.70
        +
        description_score * 0.30
    )


    return min(
        final_project_score,
        1.0
    )


# ============================================================
# QUALIFICATION MATCH
# ============================================================

def qualification_match(candidate, job):
    """
    Compare candidate qualifications with
    job qualification requirements.

    This is used for reasoning/context.
    It is not separately weighted because the
    mentor's required scoring weights already
    total 100%.
    """

    job_qualification = normalize(
        job.get(
            "qualification",
            ""
        )
    )

    if not job_qualification:

        return 0.0


    candidate_qualifications = []


    # Certifications

    candidate_qualifications.extend(
        candidate.certifications
    )


    # Education degrees

    for education in candidate.education:

        candidate_qualifications.append(
            education.degree
        )


    if not candidate_qualifications:

        return 0.0


    for qualification in candidate_qualifications:

        qualification = normalize(
            qualification
        )

        if not qualification:

            continue


        # Direct match

        if qualification in job_qualification:

            return 1.0


        # Word-level match

        qualification_words = [
            word
            for word in qualification.split()
            if len(word) > 2
        ]


        if any(
            word in job_qualification
            for word in qualification_words
        ):

            return 1.0


    return 0.0


# ============================================================
# COMPATIBILITY SCORE
# ============================================================

def calculate_compatibility_score(
    candidate,
    job
):
    """
    Calculate final compatibility score.

    Mentor-defined weights:

    Required Skills   = 40%
    Preferred Skills  = 20%
    Education         = 15%
    Experience        = 10%
    Projects          = 15%

    Total              = 100%
    """


    # --------------------------------------------------------
    # 1. Required Skills
    # --------------------------------------------------------

    required_score = skill_match(
        candidate.skills,
        job.get(
            "required_skills",
            []
        )
    )


    # --------------------------------------------------------
    # 2. Preferred Skills
    # --------------------------------------------------------

    preferred_score = skill_match(
        candidate.skills,
        job.get(
            "preferred_skills",
            []
        )
    )


    # --------------------------------------------------------
    # 3. Education
    # --------------------------------------------------------

    education_score = education_match(
        candidate,
        job
    )


    # --------------------------------------------------------
    # 4. Experience
    # --------------------------------------------------------

    experience_score = experience_match(
        candidate,
        job
    )


    # --------------------------------------------------------
    # 5. Projects
    # --------------------------------------------------------

    project_score = project_match(
        candidate,
        job
    )


    # --------------------------------------------------------
    # WEIGHTED SCORE
    # --------------------------------------------------------

    required_points = (
        required_score * 40
    )

    preferred_points = (
        preferred_score * 20
    )

    education_points = (
        education_score * 15
    )

    experience_points = (
        experience_score * 10
    )

    project_points = (
        project_score * 15
    )


    final_score = (
        required_points
        +
        preferred_points
        +
        education_points
        +
        experience_points
        +
        project_points
    )


    # Make sure score stays between 0 and 100

    final_score = max(
        0.0,
        min(
            final_score,
            100.0
        )
    )


    return round(
        final_score,
        2
    )