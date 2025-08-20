from redis.asyncio import Redis


class RedisConnector:
    def __init__(self, host: str, port: int):
        self.redis = Redis(host=host, port=port)

    async def set(self, key: str, value: str, expire: int):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.aclose()
