from fastapi import FastAPI

from routes.campaign_routes import router as campaign_router
from routes.monitoring_routes import router as monitoring_router
from routes.report_routes import router as report_router
from routes.keyword_routes import router as keyword_router
from routes.budget_routes import router as budget_router

from scheduler.monitoring_scheduler import MonitoringScheduler


##########################################################

app = FastAPI(
    title="AI Ads Intelligence Agent",
    version="1.0.0",
    description="AI Powered Google Ads Monitoring & Optimization Agent"
)

##########################################################

scheduler = MonitoringScheduler()

##########################################################


@app.on_event("startup")
def startup_event():

    scheduler.start()

    print("Monitoring Scheduler Started")


##########################################################


@app.on_event("shutdown")
def shutdown_event():

    try:

        scheduler.stop()

        print("Monitoring Scheduler Stopped")

    except Exception:

        pass


##########################################################


@app.get("/")
def root():

    return {

        "agent": "AI Ads Intelligence Agent",

        "status": "Running",

        "version": "1.0.0"

    }


##########################################################

app.include_router(
    campaign_router,
    prefix="/api/v1"
)

app.include_router(
    monitoring_router,
    prefix="/api/v1"
)

app.include_router(
    budget_router,
    prefix="/api/v1"
)

app.include_router(
    keyword_router,
    prefix="/api/v1"
)

app.include_router(
    report_router,
    prefix="/api/v1"
)