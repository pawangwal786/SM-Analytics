import logging
import time
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def check_database_health(session: AsyncSession) -> dict[str, Any]:
    """
    Checks the database health by executing a simple SELECT 1.
    Measures the latency of the query.
    """
    start_time = time.perf_counter()
    try:
        result = await session.execute(text("SELECT 1"))
        result.scalar()  # Ensure we read the result
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {"status": "up", "latency_ms": round(latency_ms, 2)}
    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "down", "latency_ms": round(latency_ms, 2), "error": str(e)}
