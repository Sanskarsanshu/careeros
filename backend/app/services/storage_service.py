"""
CareerOS — Storage Service Abstraction
"""
import os
import aiofiles
from abc import ABC, abstractmethod
from typing import BinaryIO

from app.core.config import settings


class StorageBackend(ABC):
    @abstractmethod
    async def upload(self, file_path: str, data: bytes) -> str:
        pass


class LocalStorageBackend(StorageBackend):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def upload(self, file_path: str, data: bytes) -> str:
        full_path = os.path.join(self.base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        async with aiofiles.open(full_path, "wb") as f:
            await f.write(data)
        return full_path


class S3StorageBackend(StorageBackend):
    def __init__(self):
        # Implementation deferred to Phase 2+
        pass
        
    async def upload(self, file_path: str, data: bytes) -> str:
        raise NotImplementedError("S3 storage not implemented yet.")


def get_storage_backend() -> StorageBackend:
    if settings.STORAGE_BACKEND == "local":
        return LocalStorageBackend(settings.STORAGE_LOCAL_PATH)
    return S3StorageBackend()
