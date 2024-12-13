import json

import yaml
from pydantic import BaseModel

from .llm_utils import PromptLoader
from .llm_utils.llm import OpenAIProvider
from .llm_utils.logger import get_logger
from .models import (
    ContentPrioritization,
    GapAnalysis,
    JobAnalysis,
    OptimizedResume,
    Resume,
)

logger = get_logger(__name__)


class ResumeOptimizer:
    """A class that optimizes resumes based on job descriptions using LLM.

    This class handles the multi-stage process of analyzing a job description,
    evaluating a resume against it, and generating an optimized version through
    several refinement stages.
    """

    def __init__(self, model: str = "gpt-4o"):
        """Initialize the ResumeOptimizer.

        Args:
            model (str, optional): The LLM model to use. Defaults to "gpt-4o".
        """
        self.llm = OpenAIProvider()
        self.prompts = PromptLoader("optimization")
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": self.prompts.system.render(),
            }
        ]

    def _chat_completion(
        self, message: str, response_format: dict | BaseModel = None
    ) -> str:
        """Execute a chat completion with the LLM.

        Args:
            message (str): The message to send to the LLM
            response_format (dict | BaseModel, optional): Expected response format. Defaults to None.

        Returns:
            str: The LLM's response message
        """
        self.messages.append({"role": "user", "content": message})
        assistant_message = self.llm.structured_chat_completion(
            self.messages,
            model=self.model,
            temperature=0.3,
            response_format=response_format,
        )
        self.messages.append(
            {"role": "assistant", "content": assistant_message.content}
        )
        return assistant_message

    def stage_1(self, job_description: str, user_preferences: str = None) -> str:
        """Analyze the job description and provide a structured breakdown.

        Args:
            job_description (str): The job description text to analyze

        Returns:
            str: Structured analysis of the job description
        """
        prompt = self.prompts.stage_1.render(
            job_description=job_description, user_preferences=user_preferences
        )
        return self._chat_completion(prompt, response_format=JobAnalysis)

    def stage_2(self, current_resume: Resume) -> str:
        """Analyze the current resume and provide a structured gap analysis.

        Args:
            current_resume (Resume): The resume to analyze

        Returns:
            str: Gap analysis between resume and job requirements
        """
        prompt = self.prompts.stage_2.render(
            current_resume_json=current_resume.model_dump_json(indent=2)
        )
        return self._chat_completion(prompt, response_format=GapAnalysis)

    def stage_3(self) -> str:
        """Prioritize and restructure the resume content for maximum impact.

        Returns:
            str: Content prioritization recommendations
        """
        prompt = self.prompts.stage_3.render()
        return self._chat_completion(prompt, response_format=ContentPrioritization)

    def stage_4(self) -> str:
        """Optimize the resume content with enhanced language and structure.

        Returns:
            str: Optimized resume content
        """
        prompt = self.prompts.stage_4.render()
        return self._chat_completion(prompt, response_format=OptimizedResume)

    def stage_5(self) -> Resume:
        """Generate the final optimized resume.

        Returns:
            Resume: The final optimized resume object
        """
        prompt = self.prompts.stage_5.render()
        output = self._chat_completion(prompt, response_format=Resume)
        return output

    def optimize_resume(
        self, job_description: str, current_resume: Resume, user_preferences: str = None
    ) -> Resume:
        """Execute the full resume optimization pipeline.

        This method runs through all optimization stages sequentially, from job analysis
        to final resume generation.

        Args:
            job_description (str): The target job description
            current_resume (Resume): The original resume to optimize
            user_preferences (str, optional): Additional user preferences or context. Defaults to None.

        Returns:
            Resume: The fully optimized resume
        """
        job_analysis = self.stage_1(job_description, user_preferences)
        self.print_as_yaml(job_analysis)

        gap_analysis = self.stage_2(current_resume)
        self.print_as_yaml(gap_analysis)

        content_prioritization = self.stage_3()
        self.print_as_yaml(content_prioritization)

        optimized_resume = self.stage_4()
        self.print_as_yaml(optimized_resume)

        final_resume = self.stage_5()
        self.print_as_yaml(final_resume)

        return final_resume

    @staticmethod
    def print_as_yaml(model_object: BaseModel):
        """Print structured data with proper indentation for nested elements.

        This method takes JSON data and prints it in a hierarchical format with
        proper indentation for better readability.

        Args:
            model_object (BaseModel): The model object to print.
        """
        parsed_data = model_object.model_dump(mode="python")
        yaml_str = yaml.dump(
            parsed_data,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            explicit_start=True,
        )
        logger.info(yaml_str)
