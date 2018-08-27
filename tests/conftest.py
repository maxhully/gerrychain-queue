import pytest


@pytest.fixture
def run_spec():
    return {"graph": "wisconsin", "constraints": ["contiguous"], "total_steps": 100}
