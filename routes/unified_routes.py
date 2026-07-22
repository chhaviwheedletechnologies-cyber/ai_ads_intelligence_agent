from services.agent_orchestrator import AgentOrchestrator

agent_orchestrator = AgentOrchestrator()

from fastapi import APIRouter, HTTPException

from services.google_ads_service import GoogleAdsService
from services.monitoring_service import MonitoringService
from services.budget_optimizer import BudgetOptimizer
from services.keyword_optimizer import KeywordOptimizer
from services.report_service import ReportService

router = APIRouter(prefix="/api/v1/agent", tags=["Unified"])

google_ads = GoogleAdsService()
monitoring_service = MonitoringService()
budget_optimizer = BudgetOptimizer()
keyword_optimizer = KeywordOptimizer()
report_service = ReportService()


@router.post("/run")
def run_action(action: str, campaign_id: int = None):

    if action == "list_campaigns":
        return google_ads.list_campaigns()

    elif action == "get_campaign":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        return google_ads.get_campaign(campaign_id)

    elif action == "monitor":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        return google_ads.get_campaign_metrics(campaign_id)

    elif action == "optimize_budget":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        metrics = google_ads.get_campaign_metrics(campaign_id)
        return budget_optimizer.optimize_budget(metrics)

    elif action == "get_keywords":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        return google_ads.get_keywords(campaign_id)

    elif action == "search_terms":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        return google_ads.get_search_terms(campaign_id)

    elif action == "optimize_keywords":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        return keyword_optimizer.optimize_keywords(campaign_id)  

    elif action == "get_report":
        if not campaign_id:
            raise HTTPException(400, "campaign_id required")
        return report_service.generate_report(campaign_id)

    elif action == "all_reports":
        return report_service.get_all_reports()
    
    elif action == "run_auto_optimize":
        return agent_orchestrator.process_active_campaigns()

    else:
        raise HTTPException(
            400,
            f"Unknown action '{action}'. Valid actions: list_campaigns, get_campaign, monitor, optimize_budget, get_keywords, search_terms, optimize_keywords, get_report, all_reports"
        )    