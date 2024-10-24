# CodeReviewAI

## Description

CodeReviewAI is an automatic code review tool that utilizes the OpenAI API for code analysis and the GitHub API for accessing repositories. The project is developed using Python and FastAPI and supports caching using Redis.

## Installation

To run the project, make sure you have the following dependencies installed:

- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)

### Environment Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/CodeReviewAI.git
   cd CodeReviewAI
   ```

2. Install dependencies:

    ```bash
    poetry install
    ```

3. Set up environment variables for the OpenAI and GitHub API keys:
Create a .env file in the root of the project with the following content:

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    GITHUB_API_TOKEN=your_github_token
    REDIS_HOST=your_redis_host # Default localhost
    REDIS_PORT=your_redis_port # Default 6379
    BASE_URL=your_fastapi_base_url # Example: http://localhost:8000
    ```

## Running the Application

### Start Docker Compose for Redis
To run a Redis instance, execute the following command in the root of the project:

   ```bash
   docker-compose -f docker-compose.redis.yml up -d
   ```

### Start FastAPI Application
To run the FastAPI application, use the command:

   ```bash
   poetry run uvicorn app:app --reload
   ```

### Run Unit Tests
To run the unit tests, execute the command:
   
   ```bash
   poetry run pytest tests/endpoint.py -v -s -x -W ignore::DeprecationWarning
   ```

## Usage

To use the API for code review, send a POST request to the /review endpoint with the required data:

### Example Request

   ```json
   {
   "assignment_description": "Write a function that calculates the factorial of a number.",
   "github_repo_url": "https://github.com/your_username/your_repository",
   "candidate_level": "Junior"
   }
   ```

### Example Response
   ```json
   {
     "found_files": ["main.py", "utils.py"],
     "response": "Comments:... \n\nRating: ...\n\nSummary:..."
   }
   ```