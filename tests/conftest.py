import pytest
import gerrychain_queue


@pytest.fixture
def run_spec():
    return {"graph": "wisconsin", "constraints": ["contiguous"], "total_steps": 100}


@pytest.fixture
def client():
    client = gerrychain_queue.create_app().test_client()
    yield client
