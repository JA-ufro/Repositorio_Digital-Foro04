from fastapi.testclient import TestClient

from app.main import create_app
from app.repository import SQLiteVersionRepository


def before_scenario(context, scenario):
    context.repository = SQLiteVersionRepository()
    context.client = TestClient(create_app(context.repository))
    context.version_id = None
    context.actor_role = None
    context.observation = None
    context.response = None


def after_scenario(context, scenario):
    context.repository.close()
