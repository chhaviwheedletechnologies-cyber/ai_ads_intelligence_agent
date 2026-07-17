from fastapi import APIRouter

from services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

report_service = ReportService()


##########################################################


@router.get("/{campaign_id}")
def campaign_report(campaign_id: int):

    return report_service.generate_report(campaign_id)


##########################################################


@router.get("/")
def all_reports():

    return report_service.get_all_reports()