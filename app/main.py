import asyncio

from fastapi import FastAPI
from structlog import get_logger

from app.api.ui_api.v1.video_registry_endpoint import app as video_app
from app.core.config import settings
from app.core.cron import bg_video_updater

logger = get_logger(__name__)

complete_description = (
    " This Document outlines the API contracts for for Fampay Assignment"
)

# Cron job to check & update the DB with the new video entries
logger.info("Starting the cron to add newly uploaded videos to the database.")
asyncio.create_task(bg_video_updater.insert_newly_published_videos())

app = FastAPI(title=settings.APP_NAME, description=complete_description)

app.include_router(video_app, prefix="/videos-registry/v1")
