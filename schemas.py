from typing import List
from pydantic import BaseModel


class Education(BaseModel):
    institution: str = ""
    degree: str = ""
    field: str = ""
    date: str = ""
    duration: str = ""


class Experience(BaseModel):
    position: str = ""
    organization: str = ""
    description: str = ""
    date: str = ""
    duration: str = ""


class Publication(BaseModel):
    title: str = ""
    venue: str = ""
    year: str = ""
    track: str = ""
    doi: str = ""


class CandidateProfile(BaseModel):
    skills: List[str] = []
    education: List[Education] = []
    experience: List[Experience] = []
    languages: List[str] = []
    certifications: List[str] = []
    publications: List[Publication] = []


class JobRequirements(BaseModel):
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []
    languages: List[str] = []
