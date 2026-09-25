import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from rag.query_builder import candidate_to_query
from rag.vector_store import search_jobs
from agents.scoring import calculate_compatibility_score


load_dotenv()


# --------------------------------------------------
# OpenRouter client
# --------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "openai/gpt-4o-mini"
)


# --------------------------------------------------
# Load original job dataset
# --------------------------------------------------

def load_all_jobs():
    """
    Load all internship postings from jobs.json.
    """

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------------------------
# Matching Agent
# --------------------------------------------------

def match_candidate_to_jobs(candidate, top_k=5):
    """
    Match a candidate profile against relevant
    internship postings retrieved using RAG.

    The final jobs are ranked from highest
    compatibility score to lowest.
    """

    # --------------------------------------------------
    # Step 1: Candidate → Search Query
    # --------------------------------------------------

    query = candidate_to_query(candidate)


    # --------------------------------------------------
    # Step 2: Search ChromaDB
    # --------------------------------------------------

    # Retrieve more chunks than needed because
    # multiple chunks may belong to the same job.
    retrieval_k = max(top_k * 3, 15)

    results = search_jobs(
        query,
        top_k=retrieval_k
    )


    # --------------------------------------------------
    # Step 3: Get retrieved jobs
    # --------------------------------------------------

    job_documents = results.get(
        "documents",
        [[]]
    )[0]

    job_metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    # --------------------------------------------------
    # Step 4: Load original dataset
    # --------------------------------------------------

    all_jobs = load_all_jobs()


    # Create a lookup by job ID
    jobs_by_id = {
        job["job_id"]: job
        for job in all_jobs
    }


    # --------------------------------------------------
    # Step 5: Remove duplicate jobs
    # --------------------------------------------------

    unique_jobs = {}

    for job_text, metadata in zip(
        job_documents,
        job_metadatas
    ):

        job_id = metadata.get("job_id")

        if not job_id:
            continue

        if job_id not in unique_jobs:
            unique_jobs[job_id] = {
                "job_text": job_text,
                "metadata": metadata
            }


    matched_jobs = []


    # --------------------------------------------------
    # Step 6: Calculate score for each job
    # --------------------------------------------------

    for job_id, retrieved_data in unique_jobs.items():

        job_text = retrieved_data["job_text"]

        # Find original job
        job = jobs_by_id.get(job_id)

        if not job:
            continue


        # --------------------------------------------------
        # Calculate deterministic compatibility score
        # --------------------------------------------------

        compatibility_score = (
            calculate_compatibility_score(
                candidate,
                job
            )
        )


        # --------------------------------------------------
        # Step 7: Ask LLM for reasoning
        # --------------------------------------------------

        prompt = f"""
You are an internship matching assistant.

Compare the candidate with the internship.

CANDIDATE PROFILE:
{query}

INTERNSHIP:
{job_text}

DETERMINISTIC COMPATIBILITY SCORE:
{compatibility_score}%

The score has already been calculated using:

Required Skills: 40%
Preferred Skills: 20%
Education: 15%
Experience: 10%
Projects: 15%

Do NOT change the compatibility score.

Also consider the candidate's qualifications and
the internship's responsibilities when explaining
the match.

Provide:

Matching Skills:
- List the important skills the candidate has
  that match the internship.

Missing Skills:
- List important required or preferred skills
  that the candidate does not have.

Qualification:
- Briefly explain whether the candidate's
  qualification/education is relevant.

Responsibilities:
- Briefly explain whether the candidate's
  projects or experience relate to the
  internship responsibilities.

Reason:
- Briefly explain why the candidate matches
  or does not match the internship.

Recommendation:
- Strong Match
- Good Match
- Partial Match
- Low Match

Keep the answer concise.

Do not provide another compatibility percentage.
"""


        response = client.chat.completions.create(
            model=LLM_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert internship "
                        "matching assistant."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        analysis = response.choices[0].message.content


        # --------------------------------------------------
        # Step 8: Store final result
        # --------------------------------------------------

        matched_jobs.append(
            {
                "job_id": job_id,

                "title": job.get(
                    "job_title",
                    ""
                ),

                "company": job.get(
                    "company",
                    ""
                ),

                "location": job.get(
                    "location",
                    ""
                ),

                "compatibility_score":
                    compatibility_score,

                "analysis": analysis
            }
        )


    # --------------------------------------------------
    # Step 9: Rank jobs
    # --------------------------------------------------

    matched_jobs.sort(
        key=lambda job: job["compatibility_score"],
        reverse=True
    )


    # --------------------------------------------------
    # Step 10: Return top-ranked jobs
    # --------------------------------------------------

    return matched_jobs[:top_k]