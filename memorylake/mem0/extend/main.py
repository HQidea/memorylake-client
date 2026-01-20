from typing import Any, Literal, Optional

from memorylake.mem0.client.main import AsyncMemoryClient, MemoryClient
from memorylake.mem0.client.utils import api_error_handler
from memorylake.mem0.extend.reflection import AsyncReflection, Reflection
from memorylake.mem0.memory.telemetry import capture_client_event


class MemoryLakeClient(MemoryClient):

    def new_reflection(
        self,
        target_type: Literal["user", "location"],
        target_id: str,
    ) -> Reflection:
        return Reflection(
            target_type=target_type,
            target_id=target_id,
            memory_client=self,
        )

    @api_error_handler
    def end_session(
        self,
        chat_session_id: str,
        timestamp: int,
    ) -> dict[str, Any]:
        """End a chat session.

        Args:
            chat_session_id: The ID of the chat session to end.
            timestamp: The timestamp of the session end event.

        Returns:
            A dictionary containing the API response.
        """
        payload = self._prepare_params(
            {
                "chat_session_id": chat_session_id,
                "timestamp": timestamp,
                "event_type": "end",
            }
        )
        response = self.client.post("/v3/chat_session/event/", json=payload)
        response.raise_for_status()
        capture_client_event(
            "client.end_session",
            self,
            {"chat_session_id": chat_session_id, "sync_type": "sync"},
        )
        return response.json()

    def prepare_params(self, kwargs: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        return self._prepare_params(kwargs)


class AsyncMemoryLakeClient(AsyncMemoryClient):

    def new_reflection(
        self,
        target_type: Literal["user", "location"],
        target_id: str,
    ) -> AsyncReflection:
        return AsyncReflection(
            target_type=target_type,
            target_id=target_id,
            memory_client=self,
        )

    @api_error_handler
    async def end_session(
        self,
        chat_session_id: str,
        timestamp: int,
    ) -> dict[str, Any]:
        """End a chat session.

        Args:
            chat_session_id: The ID of the chat session to end.
            timestamp: The timestamp of the session end event.

        Returns:
            A dictionary containing the API response.
        """
        payload = self._prepare_params(
            {
                "chat_session_id": chat_session_id,
                "timestamp": timestamp,
                "event_type": "end",
            }
        )
        response = await self.async_client.post("/v3/chat_session/event/", json=payload)
        response.raise_for_status()
        capture_client_event(
            "client.end_session",
            self,
            {"chat_session_id": chat_session_id, "sync_type": "async"},
        )
        return response.json()

    def prepare_params(self, kwargs: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        return self._prepare_params(kwargs)
