import json
from unittest.mock import patch, MagicMock

# import pytest


def test_post_to_runs_returns_new_run_id(client, run_spec):
    with patch("gerrychain_queue.runs.get_queue") as get_queue:
        get_queue.return_value = MagicMock()

        resp = client.post("/api/runs/", json=run_spec)
        assert resp.status_code == 200
        assert "id" in json.loads(resp.data)


def test_get_to_runs_lists_runs(client):
    with patch("gerrychain_queue.runs.get_queue") as get_queue:
        queue = MagicMock()
        get_queue.return_value = queue
        queue.list_tasks.return_value = [{"id": 12345}]

        resp = client.get("/api/runs/")
        assert resp.status_code == 200
        runs = json.loads(resp.data)
        assert isinstance(runs, list)


# @pytest.mark.integration
# def test_newly_posted_run_shows_up_in_list(client, run_spec):
#     resp = client.post("/api/runs/", json=run_spec)
#     new_run_id = json.loads(resp.data)["id"]

#     list_of_runs = json.loads(client.get("/api/runs/").data)
#     list_of_ids = [run["id"] for run in list_of_runs]

#     assert new_run_id in list_of_ids


# @pytest.mark.integration
# def test_get_status_of_a_single_run(client, run_spec):
#     response_json = json.loads(client.post("/api/runs/", json=run_spec).data)
#     run_id = response_json["id"]
#     resp = client.get("/api/runs/" + run_id)
#     assert resp.status_code == 200
#     assert "id" in json.loads(resp.data)


def test_status_of_nonexistent_run_returns_404(client):
    with patch("gerrychain_queue.runs.get_queue") as get_queue:
        queue = MagicMock()
        get_queue.return_value = queue
        queue.get_status.side_effect = KeyError()

        run_id = "fake-run-1234"
        resp = client.get("/api/runs/" + run_id)
        assert resp.status_code == 404


def test_list_of_runs_includes_hrefs_to_individual_statuses(client):
    with patch("gerrychain_queue.runs.get_queue") as get_queue:
        queue = MagicMock()
        get_queue.return_value = queue
        queue.list_tasks.return_value = [{"id": 12345}, {"id": 123456}]

        resp = client.get("/api/runs/")
        list_of_runs = json.loads(resp.data)
        assert len(list_of_runs) > 0
        assert all("href" in run.keys() for run in list_of_runs)
