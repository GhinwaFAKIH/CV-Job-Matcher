from typing import List
from pydantic import BaseModel


class CandidateProfile(BaseModel):
    skills: List[str]
    education: List[str]
    experience: List[str]
    languages: List[str]
    certifications: List[str]
    publications: List[str]


class JobRequirements(BaseModel):
    required_skills: List[str]
    preferred_skills: List[str]
    education: List[str]
    experience: List[str]
    languages: List[str]

