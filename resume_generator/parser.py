from typing import List

from .llm_utils import PromptLoader
from .llm_utils.llm import OpenAIProvider
from .llm_utils.utils import image_to_base64, pdf_to_images
from .models.resume import Resume


class ResumeParser:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = OpenAIProvider()
        self.prompts = PromptLoader("extraction")
        self.model = model

    def parse_resume(self, pdf_path: str) -> Resume:
        """
        Parses the resume and returns a Resume object.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Resume object
        """
        images = pdf_to_images(pdf_path)
        base64_images = [image_to_base64(image) for image in images]
        response = self._llm_parser(base64_images)
        return response

    def _resume_to_json(self, resume: Resume, save_path: str = None) -> str:
        """
        Converts the Resume object to a JSON string.

        Args:
            resume: Resume object

        Returns:
            JSON string
        """
        json_str = resume.model_dump_json(indent=4)
        if save_path:
            with open(save_path, "w") as f:
                f.write(json_str)
        return json_str

    def _llm_parser(self, base64_images: List[str]) -> Resume:
        response = self.llm.structured_chat_completion(
            [
                {
                    "role": "system",
                    "content": self.prompts.system.render(),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.prompts.user.render(),
                        },
                        *[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img,
                                },
                            }
                            for img in base64_images
                        ],
                    ],
                },
            ],
            model=self.model,
            response_format=Resume,
        )
        return response.parsed
