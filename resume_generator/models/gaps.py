from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SkillGap(BaseModel):
    skill: str = Field(description="Name of the skill being evaluated")
    status: str = Field(
        description="Current status of the skill - 'Present', 'Partial', or 'Missing'"
    )
    current_level: Optional[str] = Field(
        description="Current proficiency level of the skill if present"
    )
    required_level: str = Field(description="Required proficiency level for the job")
    improvement_suggestion: Optional[str] = Field(
        description="Specific suggestions for improving this skill gap"
    )


class MatchingExperience(BaseModel):
    experience: str = Field(description="Experience being evaluated")
    relevance: str = Field(
        description="Explanation of how the experience matches the job requirement"
    )


class ExperienceMatch(BaseModel):
    job_requirement: str = Field(description="Specific job requirement being evaluated")
    matching_experiences: List[MatchingExperience] = Field(
        description="List of matching experiences"
    )
    strength_level: str = Field(
        description="Overall strength of the match - 'Strong', 'Moderate', or 'Weak'"
    )
    optimization_notes: str = Field(
        description="Notes on how to better present or optimize these experiences"
    )


class TransferableSkill(BaseModel):
    current_skill: str = Field(description="Existing skill that could be transferred")
    transferable_to: str = Field(
        description="Target skill or requirement this could apply to"
    )
    relevance_explanation: str = Field(
        description="Explanation of how the current skill transfers to the target"
    )


class TerminologyAlignment(BaseModel):
    original_term: str = Field(description="Current term from resume")
    preferred_term: str = Field(description="Preferred term from job description")


class GapAnalysis(BaseModel):
    skill_gaps: List[SkillGap] = Field(
        description="List of identified skill gaps and their analysis"
    )
    experience_matches: List[ExperienceMatch] = Field(
        description="Analysis of how experiences match job requirements"
    )
    transferable_skills: List[TransferableSkill] = Field(
        description="Skills that could be reframed as relevant"
    )
    terminology_alignments: List[TerminologyAlignment] = Field(
        description="Mapping of current terms to preferred job description terms"
    )
    critical_missing_elements: List[str] = Field(
        description="Key requirements with no current match"
    )
    overall_match_score: int = Field(description="Overall match score from 0-100")
    priority_improvements: List[str] = Field(
        description="Prioritized list of suggested improvements"
    )
