from fastapi import APIRouter
from models.monitoring_models import MonitoringRequest
from services.monitoring_service import MonitoringService

router = APIRouter(tags=["Monitoring"])

service = MonitoringService()


@router.post("/monitor")

async def monitor_campaign(request: MonitoringRequest):

    return service.monitor_campaign(request)