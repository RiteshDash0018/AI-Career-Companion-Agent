from langchain_core.documents import Document


def job_to_document(job):
    """
    Convert one internship/job posting into a LangChain Document.
    """

    text = f"""
Job Title:
{job['job_title']}

Company:
{job['company']}

Location:
{job['location']}

Job Type:
{job['job_type']}

Job Description:
{job['job_description']}

Responsibilities:
{', '.join(job['responsibilities'])}

Required Skills:
{', '.join(job['required_skills'])}

Preferred Skills:
{', '.join(job['preferred_skills'])}

Qualification:
{job['qualification']}

Experience Requirements:
{job['experience_requirements']}

Education Requirements:
{job['education_requirements']}

Qualifications:
{', '.join(job.get('qualifications', []))}
"""

    return Document(
        page_content=text.strip(),
        metadata={
            "job_id": job["job_id"],
            "title": job["job_title"],
            "company": job["company"],
            "location": job["location"],
            "job_type": job["job_type"]
        }
    )