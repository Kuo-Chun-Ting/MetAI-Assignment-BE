from fastapi import APIRouter, Depends

from src.service.health_service import HealthService, get_health_service


health_router = APIRouter()


@health_router.get("/health")
def get_health(service: HealthService = Depends(get_health_service)) -> dict[str, str]:
    return service.get_health()
