import json
import requests

from schemas import CandidateProfile, JobRequirements


LLM_URL = "http://localhost:8080/v1/chat/completions"


def call_llm(prompt: str) -> dict:
    """Send a prompt to the local Qwen model and return parsed JSON."""

    response = requests.post(
        LLM_URL,
        json={
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0,
            "max_tokens": 1500
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    content = result["choices"][0]["message"]["content"].strip()

    # Remove Markdown code fences if the model adds them
    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "", 1)
        content = content.strip()

    return json.loads(content)


def extract_candidate_profile(cv_text: str) -> CandidateProfile:
    """Extract structured information from a CV."""

    prompt = f"""
You are an information extraction system.

Extract information from the CV below.

Return ONLY valid JSON with exactly these fields:

{{
    "skills": [],
    "education": [],
    "experience": [],
    "languages": [],
    "certifications": [],
    "publications": []
}}

Rules:
- Only extract information explicitly present in the CV.
- Do not invent skills, experience, education, or achievements.
- Keep the information concise.
- Return JSON only.
- Use empty lists when information is not available.

CV:
{cv_text}
"""

    data = call_llm(prompt)

    return CandidateProfile(**data)


def extract_job_requirements(job_text: str) -> JobRequirements:
    """Extract structured requirements from a job description."""

    prompt = f"""
You are an expert recruitment assistant.

Analyze the following job description and identify the qualifications
that a candidate needs for this position.

IMPORTANT:
- Extract actual requirements from the text.
- Do NOT return empty lists if the information exists.
- Python is a required skill if the job explicitly says Python skills are essential.
- Separate required qualifications from preferred qualifications.
- Include technical skills, education/background, experience, and languages.
- Do not invent information.
- Return ONLY valid JSON.
- Every item must be a short string.

Use exactly this JSON structure:

{{
    "required_skills": [],
    "preferred_skills": [],
    "education": [],
    "experience": [],
    "languages": []
}}

JOB DESCRIPTION:
{job_text[:6500]}
"""

    data = call_llm(prompt)

    return JobRequirements(**data)
