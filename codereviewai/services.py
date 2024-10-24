import base64
import fnmatch
from typing import Tuple
from urllib.parse import urlparse
import httpx
from fastapi import HTTPException, status
from .settings import settings


EXCLUDED_PATTERNS = [
    "*.yaml",
    "*.yml",
    "*.lock",
    "*.toml",
    "*.ini",
    "*.md",
    "*.pyc"
]


def is_excluded(*, filename):
    for pattern in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def get_repo_url_parts(*, url: str) -> Tuple:
    try:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")

        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo_name = path_parts[1]
            return owner, repo_name
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"Bad Request": f"Incorrect GitHub URL: {url}. "
                                       "Please enter correct url."
                                       "Example: https://github.com/<repo_owner>/<repo_name>"}
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Split error": "An error happened when splitting URL"}
        )


async def get_repository_data(*, owner: str, repo: str, path: str = ""):
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        headers = {
            "Authorization": f"Bearer {settings.GITHUB_API_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        return response.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Getting error": "An error happened when got GitHub repository"}
        )


async def get_file_data(*, file_path: str):
    try:
        headers = {
            "Authorization": f"Bearer {settings.GITHUB_API_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(file_path, headers=headers)

            file_info = response.json()
            if file_info.get("encoding") == "base64":
                try:
                    return base64.b64decode(file_info["content"]).decode("utf-8")
                except UnicodeDecodeError:
                    return base64.b64decode(file_info["content"]).decode("latin-1")
            return file_info["content"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"File error": "An error happened when reading repository file"}
        )


async def process_directory(*, owner: str, repo: str, level: str, path: str = "", files_data: list):
    content = await get_repository_data(owner=owner, repo=repo, path=path)

    for item in content:
        if is_excluded(filename=item["name"]):
            continue
        if item["type"] == "file":
            file_content = await get_file_data(file_path=item["url"])
            files_data.append({"filename": item["name"], "content": file_content, "level": level})
        elif item["type"] == "dir":
            await process_directory(
                owner=owner,
                repo=repo,
                path=item["path"],
                files_data=files_data,
                level=level
            )

