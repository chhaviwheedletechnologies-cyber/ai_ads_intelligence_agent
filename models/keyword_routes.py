from fastapi import APIRouter
from models.keyword_models import KeywordOptimizationRequest
from services.keyword_optimizer import KeywordOptimizer

router = APIRouter(tags=["Keyword"])

keyword_service = KeywordOptimizer()


@router.post("/keywords/optimize")

async def optimize_keywords(request: KeywordOptimizationRequest):

    return keyword_service.optimize(request)