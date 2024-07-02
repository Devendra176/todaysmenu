import os
from typing import List
from uuid import uuid4

from fastapi import UploadFile, HTTPException

from core.exceptions import ExceptionHandling
from core.settings import api_settings


class ContentTypeChecker:
    def __init__(self, content_types: List[str]) -> None:
        self.content_types = content_types

    async def __call__(self, files: List[UploadFile]):
        for file in files:
            if file.content_type not in self.content_types:
                raise HTTPException(status_code=400,
                                    detail=f"Invalid file type: {file.content_type}. "
                                           f"Only PNG and JPEG are allowed.")

            if file.size > api_settings.MAX_FILE_SIZE_BYTES:
                raise HTTPException(status_code=400,
                                    detail=f"File size exceeds the maximum limit of "
                                           f"{api_settings.MAX_FILE_SIZE_MB} MB.")

        return files

    async def save_files(self, files: List[UploadFile], upload_dir: str = api_settings.UPLOAD_DIR)\
            -> List[str]:

        saved_file_paths = []
        try:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            for file in files:
                file_extension = file.filename.split(".")[-1]
                unique_filename = f"{uuid4()}.{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)

                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)

                saved_file_paths.append(file_path)
        except Exception as e:
            raise ExceptionHandling(detail=str(e))
        return saved_file_paths
