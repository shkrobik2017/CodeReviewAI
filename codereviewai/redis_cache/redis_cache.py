import json
from redis import from_url
from codereviewai.schemas import ResponseSchema


class AsyncCache:
    def __init__(self, host: str, port: int, db=0):
        self.redis = from_url(f"redis://{host}:{port}/{db}", encoding="utf-8", decode_responses=True)

    def cache_data(self, key: str, data: ResponseSchema):
        if not isinstance(data, str):
            data = json.dumps(data.dict())

        self.redis.set(name=key, value=data, ex=None)

    def get_cached_data(self, key: str):
        data = self.redis.get(key)

        if data is not None:
            try:
                json_data = json.loads(data)
                return ResponseSchema(**json_data)
            except json.JSONDecodeError:
                return ResponseSchema(**data)
        return None

    def delete_cached_data(self, key):
        self.redis.delete(key)
