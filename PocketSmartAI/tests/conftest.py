import os
os.environ["USE_GEMINI"]="false"; os.environ["GEMINI_API_KEY"]=""; os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"; os.environ["SECRET_KEY"]="test-secret"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base,engine
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine); yield
@pytest.fixture
def client():
    with TestClient(app) as c: yield c
