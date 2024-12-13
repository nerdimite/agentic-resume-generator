from typing import List, Optional

from pydantic import BaseModel, Field


class JobRequirement(BaseModel):
    category: str = Field(
        description="Category of the requirement (e.g., 'Technical', 'Soft Skills', 'Experience')"
    )
    importance: str = Field(
        description="Importance level of the requirement ('Must-have' or 'Nice-to-have')"
    )
    description: str = Field(description="Detailed description of the job requirement")


class CompanyAttribute(BaseModel):
    attribute: str = Field(
        description="Type of company attribute (e.g., 'Culture', 'Values', 'Work Environment')"
    )
    description: str = Field(
        description="Detailed description of the company attribute"
    )


class JobAnalysis(BaseModel):
    role_title: str = Field(description="Title of the job role being analyzed")
    key_requirements: List[JobRequirement] = Field(
        description="List of key job requirements"
    )
    experience_level: str = Field(description="Required experience level for the role")
    primary_skills: List[str] = Field(
        description="List of primary skills needed for the job"
    )
    core_responsibilities: List[str] = Field(
        description="List of core responsibilities associated with the role"
    )
    industry_keywords: List[str] = Field(
        description="List of industry-specific keywords relevant to the job"
    )
    company_attributes: List[CompanyAttribute] = Field(
        description="List of attributes that define the company"
    )
    preferred_qualifications: List[str] = Field(
        description="List of qualifications that are preferred but not mandatory"
    )
    domain_knowledge: List[str] = Field(
        description="Specific knowledge required in the domain of the job"
    )
