from typing import Dict, List

from pydantic import BaseModel, Field


class ContentRelevance(BaseModel):
    content_type: str = Field(
        description="Type of content being evaluated (e.g., 'Experience', 'Project', 'Skill')"
    )
    content_id: str = Field(
        description="Identifier from original resume to track this content piece"
    )
    reasoning: str = Field(
        description="Explanation of why this content is relevant or not"
    )
    relevance_score: int = Field(
        description="Relevance score from 1-10, where 10 is most relevant to the job"
    )


class AchievementEnhancement(BaseModel):
    original: str = Field(description="Original achievement text from resume")
    relevance_context: str = Field(
        description="How this achievement relates to target role"
    )
    suggested_rewrite: str = Field(
        description="Suggested optimization while maintaining truthfulness"
    )
    priority: int = Field(
        description="Display priority from 1-5, where 1 is highest priority"
    )


class SectionPriority(BaseModel):
    section_name: str = Field(
        description="Name of resume section (e.g., 'Experience', 'Skills', 'Projects')"
    )
    reasoning: str = Field(description="Explanation for this prioritization")
    suggested_order: int = Field(
        description="Suggested order in final resume (1 being top)"
    )


class ContentPrioritization(BaseModel):
    content_relevance: List[ContentRelevance] = Field(
        description="Relevance analysis of each major content piece"
    )
    achievement_enhancements: List[AchievementEnhancement] = Field(
        description="Suggested improvements for achievements"
    )
    section_priorities: List[SectionPriority] = Field(
        description="Recommended organization of resume sections"
    )
    content_to_remove: List[str] = Field(
        description="Content pieces that could be removed to focus on more relevant items"
    )
    focus_keywords: List[str] = Field(
        description="Key terms/phrases that should be emphasized throughout"
    )
