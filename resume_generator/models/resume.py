from typing import List, Optional

from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    name: str = Field(description="Full name of the individual")
    email: str = Field(description="Professional email address")
    phone: str = Field(description="Contact phone number")
    location: str = Field(description="Current city/location")
    linkedin: Optional[str] = Field(description="LinkedIn profile URL", default=None)


class Experience(BaseModel):
    company: str = Field(description="Name of the organization/employer")
    title: str = Field(description="Job title/position held")
    duration: str = Field(
        description="Time period of employment (e.g., 'Jan 2020 - Present')"
    )
    location: str = Field(description="Location of the workplace")
    achievements: List[str] = Field(
        description="Key accomplishments and responsibilities in the role"
    )


class Education(BaseModel):
    degree: str = Field(description="Name of degree/certification obtained")
    institution: str = Field(description="Name of educational institution")
    duration: str = Field(description="Time period of study (e.g., '2016 - 2020')")
    gpa: Optional[str] = Field(
        description="Grade Point Average or academic performance metric", default=None
    )


class Skills(BaseModel):
    professional: List[str] = Field(
        description="Core professional and domain-specific skills"
    )
    tools: List[str] = Field(description="Software, equipment, or tools proficiency")
    soft_skills: List[str] = Field(description="Interpersonal and transferable skills")


class Project(BaseModel):
    name: str = Field(description="Title of the project")
    description: str = Field(description="Brief overview of the project and its impact")
    methodologies: List[str] = Field(
        description="Key methods, technologies, approaches, or tools used"
    )
    # TODO: extract links from pdf for additional context
    link: Optional[str] = Field(
        description="URL to project documentation or outcome.", default=None
    )


class Resume(BaseModel):
    personal_info: PersonalInfo = Field(
        description="Basic contact and identifying information"
    )
    summary: str = Field(
        description="Brief professional summary or objective statement"
    )
    experience: List[Experience] = Field(description="Professional work history")
    education: List[Education] = Field(
        description="Academic background and qualifications"
    )
    skills: Skills = Field(description="Professional capabilities and competencies")
    projects: List[Project] = Field(description="Notable projects and achievements")
