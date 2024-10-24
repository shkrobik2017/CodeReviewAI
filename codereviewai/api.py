from fastapi import APIRouter, status, HTTPException

from .agent.agent import generate_llm_response
from .redis_cache.redis_cache import AsyncCache
from .schemas import ResponseSchema, ReviewRequest
from .services import get_repo_url_parts, process_directory
from .settings import settings

router = APIRouter()


@router.post(
    path="/review",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema
)
async def get_code_review(
        request: ReviewRequest
):
    """
    This endpoint for generate LLM response with comment and rating code.

    It takes ReviewRequest schema with following params:

    :param request:
    assignment_description: str - description of repository task
    github_repo_url: str - GitHub repository URL
    candidate_level: str - Candidate level (Junior, Middle, Senior)
    :return:
    files_found: list - list of analysed files
    response: str - LLM response
    """
    redis = AsyncCache(
        settings.REDIS_HOST,
        settings.REDIS_PORT
    )

    if request.candidate_level.lower() not in ["junior", "middle", "senior"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "Bad request": f"Candidate level must be Junior, Middle or Senior. "
                               f"Your value: {request.candidate_level}"
            }
        )

    files_data = []
    repo_owner, repo_name = get_repo_url_parts(url=request.github_repo_url)

    if cached_data := redis.get_cached_data(repo_name):
        return cached_data

    await process_directory(
        owner=repo_owner,
        repo=repo_name,
        files_data=files_data,
        level=request.candidate_level
    )

    llm_request = "\n-----------------------------------------------\n".join(
        [item["content"] for item in files_data]
    )
    llm_response = generate_llm_response(
        files_data=llm_request,
        assignment_description=request.assignment_description,
        candidate_level=request.candidate_level
    )

    response = ResponseSchema(
        files_found=[item["filename"] for item in files_data],
        response=llm_response
    )

    redis.cache_data(
        key=repo_name,
        data=response
    )

    return response
