import pytest
from unittest.mock import MagicMock
from gerrychain_queue.queue import Queue


@pytest.fixture
def queue():
    Redis = MagicMock()
    Task = MagicMock()
    return Queue(dict(), key="queue", Cache=Redis, Task=Task)


def test_list_of_runs_includes_statuses(queue):
    list_of_runs = queue.list_tasks()
    assert all("status" in run.keys() for run in list_of_runs)
