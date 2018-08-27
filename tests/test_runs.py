import json

import pytest
import gerrychain_queue


@pytest.fixture
def client():
    client = gerrychain_queue.create_app().test_client()
    yield client


def test_post_to_runs_returns_new_run_id(client):
    resp = client.post("/runs/")
    assert resp.status_code == 200
    assert "id" in json.loads(resp.data)


def test_get_to_runs_lists_runs(client):
    resp = client.get("/runs/")
    assert resp.status_code == 200
    runs = json.loads(resp.data)
    assert isinstance(runs, list)


def test_newly_posted_run_shows_up_in_list(client):
    resp = client.post("/runs/")
    new_run_id = json.loads(resp.data)["id"]
    list_of_runs = json.loads(client.get("/runs/").data)
    list_of_ids = [run["id"] for run in list_of_runs]
    assert new_run_id in list_of_ids


def test_get_status_of_a_single_run(client):
    run_id = json.loads(client.post("/runs/").data)["id"]

    resp = client.get("/runs/" + run_id)
    assert resp.status_code == 200
    assert "id" in json.loads(resp.data)


def test_status_of_nonexistent_run_returns_404(client):
    run_id = "fake-run-1234"

    resp = client.get("/runs/" + run_id)
    assert resp.status_code == 404