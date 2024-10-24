from fastapi import HTTPException, status
from openai import OpenAI
from codereviewai.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_role_assistant():
    with open("codereviewai/agent/role_description.md", "r") as file:
        return file.read()


def generate_llm_response(*, files_data: str, assignment_description: str, candidate_level: str):
    try:
        role = get_role_assistant()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": files_data},
                {"role": "system", "content": role.format(assignment_description, candidate_level)},
            ]
        )
        result = completion.choices[0].message.content
        return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"LLM Error": "An error happened when LLM generate response"}
        )
