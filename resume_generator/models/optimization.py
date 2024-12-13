from typing import Dict, List

from pydantic import BaseModel, Field


class OptimizedBulletPoint(BaseModel):
    original: str = Field(description="Original bullet point from the resume")
    optimized: str = Field(
        description="Enhanced version with better impact statements and relevant keywords"
    )
    keywords_added: List[str] = Field(
        description="Job-specific keywords naturally incorporated"
    )


class OptimizedExperience(BaseModel):
    company: str = Field(description="Company name from original resume")
    title: str = Field(
        description="Position title, possibly refined to align with target role terminology"
    )
    duration: str = Field(description="Employment duration")
    optimized_achievements: List[OptimizedBulletPoint] = Field(
        description="Enhanced bullet points for this experience"
    )
    priority_order: int = Field(
        description="Display order within experience section (1 being highest)"
    )


class OptimizedProject(BaseModel):
    name: str = Field(description="Project name, possibly refined for clarity")
    description: str = Field(
        description="Enhanced project description highlighting relevant aspects"
    )
    technologies: List[str] = Field(
        description="Technologies used, aligned with job requirements"
    )
    impact_statement: str = Field(
        description="Quantified or qualified impact of the project"
    )


class OptimizedSkillCategory(BaseModel):
    category: str = Field(
        description="Skill category (e.g., 'Technical', 'Tools', 'Soft Skills')"
    )
    skills: List[str] = Field(
        description="List of skills in this category, ordered by relevance to job"
    )
    relevance_score: float = Field(
        description="Category relevance score to job requirements (0-1)"
    )


class OptimizedResume(BaseModel):
    summary: str = Field(
        description="Tailored professional summary highlighting key relevant qualifications"
    )
    experiences: List[OptimizedExperience] = Field(
        description="Optimized work experiences in priority order"
    )
    skills: List[OptimizedSkillCategory] = Field(
        description="Reorganized skills categorized and prioritized for the role"
    )
    projects: List[OptimizedProject] = Field(
        description="Optimized projects highlighting relevant technologies and impacts"
    )
    keyword_density_score: float = Field(
        description="Score between 0-1 indicating natural keyword integration"
    )
