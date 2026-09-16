from models.candidate import CandidateProfile


def candidate_to_query(candidate: CandidateProfile) -> str:
    """
    Convert a candidate profile into a natural-language
    search query for semantic internship retrieval.
    """

    query_parts = []

    # Skills
    if candidate.skills:
        query_parts.append(
            "Skills: " + ", ".join(candidate.skills)
        )

    # Education
    if candidate.education:
        education_text = []

        for education in candidate.education:
            education_text.append(
                f"{education.degree} "
                f"from {education.institution} "
                f"({education.year})"
            )

        query_parts.append(
            "Education: " + "; ".join(education_text)
        )

    # Experience
    if candidate.experience:
        experience_text = []

        for experience in candidate.experience:
            experience_text.append(
                f"{experience.role} at "
                f"{experience.company} "
                f"for {experience.duration}"
            )

        query_parts.append(
            "Experience: " + "; ".join(experience_text)
        )

    # Projects
    if candidate.projects:
        project_text = []

        for project in candidate.projects:
            technologies = ", ".join(
                project.technologies
            )

            project_text.append(
                f"{project.name}: "
                f"{project.description}. "
                f"Technologies: {technologies}"
            )

        query_parts.append(
            "Projects: " + "; ".join(project_text)
        )

    # Certifications
    if candidate.certifications:
        query_parts.append(
            "Certifications: "
            + ", ".join(candidate.certifications)
        )

    # Career interests
    if candidate.career_interests:
        query_parts.append(
            "Career Interests: "
            + ", ".join(candidate.career_interests)
        )

    return "\n".join(query_parts)