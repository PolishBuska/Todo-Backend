from fastapi import APIRouter

health = APIRouter(

)


@health.get('/health')
async def healthcheck(a: str):
    return {
        "health": "healthy",
        "suggestions": "Can proceed with further requests",
        "overall": "app is healthy, web server is running",
        "param": a
    }
