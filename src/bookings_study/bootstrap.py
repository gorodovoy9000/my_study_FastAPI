from bookings_study.connectors.redis_connector import RedisConnector
from bookings_study.config import settings

redis_connector = RedisConnector(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
