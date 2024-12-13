from typing import Any, AsyncIterator, List, Optional

from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from pydantic import BaseModel, Field
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class LLMError(Exception):
    """Base exception class for LLM API errors"""

    pass


class ChatMessage(BaseModel):
    """Pydantic model for chat messages"""

    role: str = Field(
        ..., description="The role of the message sender (system, user, assistant)"
    )
    content: str = Field(..., description="The content of the message")
    name: Optional[str] = Field(None, description="The name of the sender (optional)")


def get_default_retry_decorator():
    """Get the default retry decorator with standard settings"""
    return retry(
        retry=retry_if_exception_type(
            Exception
        ),  # Base implementation retries on any exception
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
    )


class BaseProvider:
    """Base class for LLM providers with retry functionality"""

    def __init__(self, retry_decorator=None):
        self._retry_decorator = retry_decorator or get_default_retry_decorator()
        # Apply retry decorator to methods
        self.chat_completion = self._retry_decorator(self.chat_completion)
        self.achat_completion = self._retry_decorator(self.achat_completion)

    @property
    def retry_decorator(self):
        return self._retry_decorator

    @retry_decorator.setter
    def retry_decorator(self, decorator):
        self._retry_decorator = decorator
        # Reapply retry decorator to methods
        self.chat_completion = self._retry_decorator(self.chat_completion)
        self.achat_completion = self._retry_decorator(self.achat_completion)

    def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> ChatCompletion:
        """To be implemented by subclasses"""
        raise NotImplementedError

    async def achat_completion(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> ChatCompletion | AsyncIterator[ChatCompletionChunk]:
        """To be implemented by subclasses"""
        raise NotImplementedError
