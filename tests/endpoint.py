import httpx
import pytest
from ..codereviewai.settings import settings


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "request_data,expected_status",
    [
        (
            {
                "assignment_description": "Task of the project is to create a simple library data managing code",
                "github_repo_url": "https://github.com/shkrobik2017/SQLAlchemyPet",
                "candidate_level": "Junior"
            },
            200
        ),
        (
            {
                "assignment_description": "Task of the project is to create a simple library data managing code",
                "github_repo_url": "https://github.com/shkrobik2017/SQLAlchemyPet",
                "candidate_level": "Lead"
            },
            400
        ),
        (
            {
                "assignment_description": "Task of the project is to create a simple library data managing code",
                "github_repo_url": "https://github.com/shkrobik2017/SQLAlchemyPet",
                "candidate_level": 555
            },
            422
        )
    ]
)
async def test_generate_response_success(request_data, expected_status):
    async with httpx.AsyncClient(base_url=settings.BASE_URL, timeout=60) as client:
        response = await client.post(
            url="/review",
            json=request_data
        )

        assert response.status_code == expected_status
