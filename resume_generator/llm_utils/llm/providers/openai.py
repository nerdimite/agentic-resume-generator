from typing import Any, Dict, List, Optional

import openai
from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel

from ...logger import get_logger, log_execution
from .base import BaseProvider, ChatMessage, LLMError

logger = get_logger("openai")


def get_openai_retry_decorator():
    """Get OpenAI-specific retry decorator"""
    from tenacity import (
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

    return retry(
        retry=retry_if_exception_type(
            (openai.RateLimitError, openai.APIError, openai.APIConnectionError)
        ),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
    )


class OpenAIProvider(BaseProvider):
    """OpenAI implementation of the LLM provider interface"""

    def __init__(self, api_key: Optional[str] = None, retry_decorator=None):
        super().__init__(retry_decorator or get_openai_retry_decorator())
        self.sync_client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)

    def _prepare_params(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Prepare parameters for API call"""
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            **kwargs,
        }
        if max_tokens:
            params["max_tokens"] = max_tokens
        return params

    @log_execution(logger=logger)
    def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = "gpt-4o-2024-08-06",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Synchronously call OpenAI's chat completions API with retry functionality.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            API response

        Raises:
            LLMError: If the API call fails after all retry attempts
        """
        try:
            params = self._prepare_params(
                messages, model, temperature, max_tokens, **kwargs
            )
            return self.sync_client.chat.completions.create(**params)
        except (openai.RateLimitError, openai.APIError, openai.APIConnectionError) as e:
            raise e
        except Exception as e:
            raise LLMError(f"Error calling OpenAI API: {str(e)}")

    @log_execution(logger=logger)
    async def achat_completion(
        self,
        messages: List[ChatMessage],
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Asynchronously call OpenAI's chat completions API with retry functionality.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            API response

        Raises:
            LLMError: If the API call fails after all retry attempts
        """
        try:
            params = self._prepare_params(
                messages, model, temperature, max_tokens, **kwargs
            )
            return await self.async_client.chat.completions.create(**params)
        except (openai.RateLimitError, openai.APIError, openai.APIConnectionError) as e:
            raise e
        except Exception as e:
            raise LLMError(f"Error calling OpenAI API: {str(e)}")

    @log_execution(logger=logger)
    def structured_chat_completion(
        self,
        messages: List[ChatMessage],
        response_format: type[BaseModel],
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Synchronously call OpenAI's structured chat completions API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            response_format: Pydantic model class defining the expected response structure
            model: OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Parsed response matching the provided Pydantic model

        Raises:
            LLMError: If the API call fails after all retry attempts
        """
        try:
            params = self._prepare_params(
                messages, model, temperature, max_tokens, **kwargs
            )
            return (
                self.sync_client.beta.chat.completions.parse(
                    response_format=response_format, **params
                )
                .choices[0]
                .message
            )
        except (openai.RateLimitError, openai.APIError, openai.APIConnectionError) as e:
            raise e
        except Exception as e:
            raise LLMError(f"Error calling OpenAI API: {str(e)}")

    @log_execution(logger=logger)
    async def astructured_chat_completion(
        self,
        messages: List[ChatMessage],
        response_format: type[BaseModel],
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Asynchronously call OpenAI's structured chat completions API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            response_format: Pydantic model class defining the expected response structure
            model: OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Parsed response matching the provided Pydantic model

        Raises:
            LLMError: If the API call fails after all retry attempts
        """
        try:
            params = self._prepare_params(
                messages, model, temperature, max_tokens, **kwargs
            )
            return (
                await self.async_client.beta.chat.completions.parse(
                    response_format=response_format, **params
                )
                .choices[0]
                .message
            )
        except (openai.RateLimitError, openai.APIError, openai.APIConnectionError) as e:
            raise e
        except Exception as e:
            raise LLMError(f"Error calling OpenAI API: {str(e)}")
