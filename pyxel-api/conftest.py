# import sys
# import os
# import pytest

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from api import app as flask_app

# @pytest.fixture
# def client():
#     flask_app.config["TESTING"] = True
#     with flask_app.test_client() as client:
#         yield client



import sys
import os
import pytest
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Point to the TEST database before importing api.py / database.py,
# so tests never touch the real production database.
test_db_url = os.environ.get("TEST_DATABASE_URL")
if not test_db_url:
    raise RuntimeError("TEST_DATABASE_URL is not set — refusing to run tests against production DB")
os.environ["DATABASE_URL"] = test_db_url

from api import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client