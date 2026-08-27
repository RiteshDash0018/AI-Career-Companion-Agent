from pydantic import BaseModel, Field, field_validator
from typing import List


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)

    @field_validator("technologies", mode="before")
    @classmethod
    def convert_technologies_to_list(cls, value):

        # If already a list, keep it
        if isinstance(value, list):
            return value

        # If LLM returns a string
        if isinstance(value, str):

            # Convert:
            # "Python, Deep Learning"
            # into:
            # ["Python", "Deep Learning"]

            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        # If nothing is provided
        return []


class CandidateProfile(BaseModel):

    name: str = ""

    email: str = ""

    phone: str = ""

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(
        default_factory=list
    )

    experience: List[Experience] = Field(
        default_factory=list
    )

    projects: List[Project] = Field(
        default_factory=list
    )

    certifications: List[str] = Field(
        default_factory=list
    )

    career_interests: List[str] = Field(
        default_factory=list
    )