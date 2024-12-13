import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.run import Run
from openai.types.file_object import FileObject

from ..logger import get_logger

DEFAULT_MODEL = os.getenv("OAI_ASSISTANT_MODEL", "gpt-4o-2024-08-06")
DEFAULT_POLL_INTERVAL_MS = 1000
DEFAULT_ID_LOG_FILE = os.path.join(os.path.dirname(__file__), "assistants_id_logs.csv")


logger = get_logger(__name__)


class IDLogger:
    """
    Logs the IDs of created Assistants API objects (Threads, Files, Assistants) to a CSV file.

    Why?
    OpenAI Assistants API does not provide a way to retrieve all the IDs of created objects.
    So it's better to log them to a file ourselves and clean them up if needed.
    """

    def __init__(self, csv_file_path: str = DEFAULT_ID_LOG_FILE) -> None:
        """
        Initialize the IDLogger with a CSV file path.

        Args:
            csv_file_path (str): Path to the CSV file where IDs will be logged. Defaults to DEFAULT_ID_LOG_FILE.
        """
        self.csv_file_path = csv_file_path
        if not os.path.exists(csv_file_path):
            self.csv_file = open(csv_file_path, "w")
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(["datetime", "type", "id"])
            self.is_new = True
        else:
            self.csv_file = open(csv_file_path, "a")
            self.csv_writer = csv.writer(self.csv_file)
            self.is_new = False

    def log_id(self, object: Union[FileObject, Assistant, Thread]) -> None:
        """
        Log an object's ID to the CSV file if it hasn't been logged before.

        Args:
            object (Union[FileObject, Assistant, Thread]): The object whose ID should be logged.
        """
        if not self.is_new:
            existing_rows = self.retrieve_all()
            existing_ids = [row["id"] for row in existing_rows]
            if object.id in existing_ids:
                return

        self.csv_writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                object.__class__.__name__,
                object.id,
            ]
        )
        self.csv_file.flush()

    def retrieve_all(self) -> List[Dict[str, str]]:
        """
        Retrieve all logged entries from the CSV file.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing the logged entries.
        """
        with open(self.csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            return [dict(zip(header, row)) for row in csv_reader]

    def delete_all(self) -> None:
        """
        Delete all objects logged in the CSV file from OpenAI and clear the log.
        """
        if not self.is_new:
            client = OpenAI()
            rows = self.retrieve_all()
            for row in rows:
                if row["type"] == "Thread":
                    client.beta.threads.delete(row["id"])
                elif row["type"] == "FileObject":
                    client.files.delete(row["id"])
                elif row["type"] == "Assistant":
                    client.beta.assistants.delete(row["id"])

            # Remove all rows from the CSV file
            self.csv_file.close()
            with open(self.csv_file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["datetime", "type", "id"])
            self.csv_file = open(self.csv_file_path, "a")
            self.csv_writer = csv.writer(self.csv_file)


class OpenAIAssistant:
    """
    A wrapper around the OpenAI Assistants API for easier interaction with common utility methods.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        system_instructions: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        assistant_id: Optional[str] = None,
        tools: Optional[List[Dict[str, str]]] = [{"type": "code_interpreter"}],
    ) -> None:
        """
        Initialize the OpenAI Assistant.

        Args:
            name (Optional[str]): Name of the assistant. Defaults to None.
            system_instructions (Optional[str]): System instructions for the assistant. Defaults to None.
            model (str): Model to use. Defaults to DEFAULT_MODEL.
            assistant_id (Optional[str]): ID of existing assistant to load. Defaults to None.
            tools (Optional[List[Dict[str, str]]]): List of tools for the assistant. Defaults to [{"type": "code_interpreter"}].
        """
        self.client = OpenAI()

        self._assistant = None
        self._thread = None
        self._files = []

        self._id_logger = IDLogger()

        # If assistant_id is provided, load the assistant instead of creating a new one
        if assistant_id:
            self._assistant = self.load_assistant(assistant_id)
            self.log_id(self._assistant)
        else:
            self._assistant = self.create_assistant(
                name=name,
                instructions=system_instructions,
                tools=tools,
                model=model,
            )
            self.log_id(self._assistant)

    def log_id(self, object: Union[FileObject, Assistant, Thread]) -> None:
        """
        Log an object's ID using the ID logger.

        Args:
            object (Union[FileObject, Assistant, Thread]): Object whose ID should be logged.
        """
        self._id_logger.log_id(object)

    def create_assistant(
        self,
        name: str,
        instructions: str,
        tools: Optional[List[Dict[str, str]]],
        model: str = DEFAULT_MODEL,
        **kwargs: Any,
    ) -> Assistant:
        """
        Create a new OpenAI Assistant.

        Args:
            name (str): Name of the assistant.
            instructions (str): System instructions for the assistant.
            tools (Optional[List[Dict[str, str]]]): List of tools for the assistant.
            model (str): Model to use. Defaults to DEFAULT_MODEL.
            **kwargs (Any): Additional arguments to pass to the create call.

        Returns:
            Assistant: The created assistant object.
        """
        return self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools,
            **kwargs,
        )

    def load_assistant(self, assistant_id: str) -> Assistant:
        """
        Load an existing OpenAI Assistant.

        Args:
            assistant_id (str): ID of the assistant to load.

        Returns:
            Assistant: The loaded assistant object.
        """
        return self.client.beta.assistants.retrieve(assistant_id)

    def upload_file(self, file_path: Union[str, Path]) -> FileObject:
        """
        Upload a file to be used with the assistant.

        Args:
            file_path (Union[str, Path]): Path to the file to upload.

        Returns:
            FileObject: The uploaded file object.
        """
        file = self.client.files.create(
            file=open(file_path, "rb"), purpose="assistants"
        )
        self._files.append(file)
        self.log_id(file)
        logger.info(f"Uploaded file: {file.id}")

        return file

    def load_file(self, file_id: str) -> FileObject:
        """
        Load an existing file by ID.

        Args:
            file_id (str): ID of the file to load.

        Returns:
            FileObject: The loaded file object.
        """
        return self.client.files.retrieve(file_id)

    def create_or_load_thread(
        self, thread_id: Optional[str] = None, **kwargs: Any
    ) -> None:
        """
        Create a new thread or load an existing one.

        Args:
            thread_id (Optional[str]): ID of existing thread to load. Defaults to None.
            **kwargs (Any): Additional arguments for thread creation.
        """
        if thread_id:
            self._thread = self.load_thread(thread_id)
            logger.info(f"Loaded thread: {self._thread.id}")
        else:
            self._thread = self.create_thread(**kwargs)
            logger.info(f"Created thread: {self._thread.id}")

        self.log_id(self._thread)

    def load_thread(self, thread_id: str) -> Thread:
        """
        Load an existing thread by ID.

        Args:
            thread_id (str): ID of the thread to load.

        Returns:
            Thread: The loaded thread object.
        """
        return self.client.beta.threads.retrieve(thread_id)

    def create_thread(self, **kwargs: Any) -> Thread:
        """
        Create a new thread.

        Args:
            **kwargs (Any): Arguments for thread creation.

        Returns:
            Thread: The created thread object.
        """
        return self.client.beta.threads.create(**kwargs)

    def add_message(
        self,
        message: str,
        role: Literal["user", "assistant"] = "user",
        **kwargs: Any,
    ) -> None:
        """
        Add a message to the current thread.

        Args:
            message (str): Content of the message.
            role (Literal["user", "assistant"]): Role of the message sender. Defaults to "user".
            **kwargs (Any): Additional arguments for message creation.
        """
        self.client.beta.threads.messages.create(
            thread_id=self._thread.id,
            role=role,
            content=message,
            **kwargs,
        )

    def run_thread_with_polling(
        self, poll_interval_ms: int = DEFAULT_POLL_INTERVAL_MS, **kwargs: Any
    ) -> Tuple[Run, Message]:
        """
        Run the current thread and poll for completion.

        Args:
            poll_interval_ms (int): Polling interval in milliseconds. Defaults to DEFAULT_POLL_INTERVAL_MS.
            **kwargs (Any): Additional arguments for run creation.

        Returns:
            Tuple[Run, Message]: The completed run object and the last message.
        """
        logger.info(f"Running thread: {self._thread.id}")
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self._thread.id,
            assistant_id=self._assistant.id,
            poll_interval_ms=poll_interval_ms,
            **kwargs,
        )
        logger.info(f"Run completed: {run.id}")
        messages = self.get_all_messages()
        last_message = messages[-1]

        return run, last_message

    def get_all_messages(self) -> List[Message]:
        """
        Get all messages from the current thread.

        Returns:
            List[Message]: List of messages in reverse chronological order.
        """
        messages = self.client.beta.threads.messages.list(thread_id=self._thread.id)
        return messages.data[::-1]
