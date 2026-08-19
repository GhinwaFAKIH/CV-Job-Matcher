from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from schemas import CandidateProfile, JobRequirements


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

model = SentenceTransformer(MODEL_NAME)


def semantic_similarity(text1: str, text2: str) -> float:
    embeddings = model.encode([text1, text2])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)


def classify_score(score: float) -> str:
    if score >= 0.75:
        return "Strong"

    if score >= 0.50:
        return "Partial"

    return "Weak"


def match_items(candidate_items, job_items):
    results = []

    for job_item in job_items:

        best_match = None
        best_score = 0.0

        for candidate_item in candidate_items:

            score = semantic_similarity(
                job_item,
                candidate_item
            )

            if score > best_score:
                best_score = score
                best_match = candidate_item

        results.append({
            "requirement": job_item,
            "candidate_match": best_match,
            "score": round(best_score, 3),
            "classification": classify_score(best_score)
        })

    return results


def calculate_category_score(results):
    if not results:
        return 0.0

    return sum(r["score"] for r in results) / len(results)


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

    required_score = calculate_category_score(
        required_skill_matches
    )

    preferred_score = calculate_category_score(
        preferred_skill_matches
    )

    education_score = calculate_category_score(
        education_matches
    )

    experience_score = calculate_category_score(
        experience_matches
    )

    language_score = calculate_category_score(
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
        "overall_score": round(overall_score * 100, 1),

        "required_skills": required_skill_matches,

        "preferred_skills": preferred_skill_matches,

        "education": education_matches,

        "experience": experience_matches,

        "languages": language_matches
    }
