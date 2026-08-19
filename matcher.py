import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from schemas import CandidateProfile, JobRequirements


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

model = SentenceTransformer(MODEL_NAME)


def normalize(text: str) -> str:
    """Normalize text for keyword comparison."""

    text = text.lower()

    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9+#.]+", " ", text)

    return text.strip()


def exact_match(requirement: str, candidate: str) -> bool:
    """Check whether the requirement explicitly appears in the candidate text."""

    req = normalize(requirement)
    cand = normalize(candidate)

    return req in cand


def semantic_similarity(text1: str, text2: str) -> float:

    embeddings = model.encode(
        [text1, text2],
        normalize_embeddings=True
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)


def calculate_match_score(requirement: str, candidate: str):

    # Exact match gets highest confidence
    if exact_match(requirement, candidate):

        return 1.0, "Exact"

    # Otherwise use semantic similarity
    score = semantic_similarity(
        requirement,
        candidate
    )

    if score >= 0.70:
        classification = "Strong"

    elif score >= 0.50:
        classification = "Partial"

    else:
        classification = "Weak"

    return score, classification


def match_items(candidate_items, job_items):

    results = []

    for job_item in job_items:

        best_match = None
        best_score = 0.0
        best_classification = "Weak"

        for candidate_item in candidate_items:

            score, classification = calculate_match_score(
                job_item,
                candidate_item
            )

            if score > best_score:

                best_score = score
                best_match = candidate_item
                best_classification = classification

        results.append({

            "requirement": job_item,

            "candidate_match": best_match,

            "score": round(best_score, 3),

            "classification": best_classification

        })

    return results


def category_score(results):

    if not results:
        return 0.0

    return sum(
        r["score"]
        for r in results
    ) / len(results)


def match_candidate_to_job(
    candidate: CandidateProfile,
    job: JobRequirements
):

    required_skill_matches = match_items(
        candidate.skills,
        job.required_skills
    )

    preferred_skill_matches = match_items(
        candidate.skills,
        job.preferred_skills
    )

    education_matches = match_items(
        [
            f"{e.degree} {e.field} {e.institution}"
            for e in candidate.education
        ],
        job.education
    )

    experience_matches = match_items(
        [
            f"{e.position} {e.organization} {e.description}"
            for e in candidate.experience
        ],
        job.experience
    )

    language_matches = match_items(
        candidate.languages,
        job.languages
    )

    required_score = category_score(
        required_skill_matches
    )

    preferred_score = category_score(
        preferred_skill_matches
    )

    education_score = category_score(
        education_matches
    )

    experience_score = category_score(
        experience_matches
    )

    language_score = category_score(
        language_matches
    )

    overall_score = (

        required_score * 0.50

        + experience_score * 0.20

        + education_score * 0.15

        + language_score * 0.10

        + preferred_score * 0.05

    )

    return {

        "overall_score":
            round(overall_score * 100, 1),

        "required_skills":
            required_skill_matches,

        "preferred_skills":
            preferred_skill_matches,

        "education":
            education_matches,

        "experience":
            experience_matches,

        "languages":
            language_matches

    }
