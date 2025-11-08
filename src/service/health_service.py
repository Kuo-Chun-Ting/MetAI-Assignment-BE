class HealthService:
    def get_health(self) -> dict[str, str]:
        return {"message": "Hello World", "status": "healthy"}


def get_health_service() -> HealthService:
    return HealthService()
