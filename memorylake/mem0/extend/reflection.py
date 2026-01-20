import uuid
from typing import TYPE_CHECKING, Any, Literal, Optional

from memorylake.mem0.client.utils import api_error_handler
from memorylake.mem0.memory.telemetry import capture_client_event

if TYPE_CHECKING:
    from memorylake.mem0.extend.main import AsyncMemoryLakeClient, MemoryLakeClient


class Reflection:

    def __init__(
        self,
        target_type: Literal["user", "location"],
        target_id: str,
        memory_client: "MemoryLakeClient",
    ):
        self.target_type = target_type
        self.target_id = target_id
        self.memory_client = memory_client
        self.reflect_id = str(uuid.uuid4())

    @api_error_handler
    def recollect(self, **kwargs) -> dict[str, Any]:
        metadata = kwargs.get("metadata") or {}
        user_extension = metadata.get("memorylake_extension") or {}
        metadata["memorylake_extension"] = {
            **user_extension,
            "reflect_id": self.reflect_id,
            "reflect_target": {
                "target_type": self.target_type,
                "target_id": self.target_id,
            },
        }
        kwargs["metadata"] = metadata
        payload = self.memory_client.prepare_params(kwargs)
        response = self.memory_client.client.post("/v3/memories/recollect/", json=payload)
        response.raise_for_status()
        capture_client_event(
            "client.recollect",
            self.memory_client,
            {"reflect_id": self.reflect_id, "sync_type": "sync"},
        )
        return response.json()

    def save(self, messages, **kwargs) -> dict[str, Any]:
        metadata = kwargs.get("metadata") or {}
        user_extension = metadata.get("memorylake_extension") or {}
        metadata["memorylake_extension"] = {
            **user_extension,
            "reflect_id": self.reflect_id,
            "reflect_target": {
                "target_type": self.target_type,
                "target_id": self.target_id,
            },
        }
        kwargs["metadata"] = metadata
        return self.memory_client.add(messages, **kwargs)


class AsyncReflection:

    def __init__(
        self,
        target_type: Literal["user", "location"],
        target_id: str,
        memory_client: "AsyncMemoryLakeClient",
    ):
        self.target_type = target_type
        self.target_id = target_id
        self.memory_client = memory_client
        self.reflect_id = str(uuid.uuid4())

    @api_error_handler
    async def recollect(self, **kwargs) -> dict[str, Any]:
        metadata = kwargs.get("metadata") or {}
        user_extension = metadata.get("memorylake_extension") or {}
        metadata["memorylake_extension"] = {
            **user_extension,
            "reflect_id": self.reflect_id,
            "reflect_target": {
                "target_type": self.target_type,
                "target_id": self.target_id,
            },
        }
        kwargs["metadata"] = metadata
        payload = self.memory_client.prepare_params(kwargs)
        response = await self.memory_client.async_client.post("/v3/memories/recollect/", json=payload)
        response.raise_for_status()
        capture_client_event(
            "client.recollect",
            self.memory_client,
            {"reflect_id": self.reflect_id, "sync_type": "async"},
        )
        return response.json()

    async def save(self, messages, **kwargs) -> dict[str, Any]:
        metadata = kwargs.get("metadata") or {}
        user_extension = metadata.get("memorylake_extension") or {}
        metadata["memorylake_extension"] = {
            **user_extension,
            "reflect_id": self.reflect_id,
            "reflect_target": {
                "target_type": self.target_type,
                "target_id": self.target_id,
            },
        }
        kwargs["metadata"] = metadata
        return await self.memory_client.add(messages, **kwargs)
