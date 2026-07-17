from fastapi import APIRouter
from models.report_models import ReportRequest
from services.report_service import ReportService

router = APIRouter(tags=["Reports"])

report_service = ReportService()


@router.post("/report")

async def generate_report(request: ReportRequest):

    return report_service.generate(request)