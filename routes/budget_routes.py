from fastapi import APIRouter
from models.budget_models import BudgetOptimizationRequest
from services.budget_optimizer import BudgetOptimizer

router = APIRouter(tags=["Budget"])

budget_service = BudgetOptimizer()


@router.post("/budget/optimize")
async def optimize_budget(request: BudgetOptimizationRequest):

    metrics = {
        "cost": request.current_spend,
        "conversions": getattr(request, "conversions", 0),
        "cpa": request.current_cpa,
        "roas": request.current_roas,
        "current_budget": request.current_budget,
    }

    recommendations = budget_service.optimize_budget(metrics)

    return {
        "status": "success",
        "campaign_id": request.campaign_id,
        "recommendations": recommendations
    }