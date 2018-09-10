import pytest
from unittest.mock import MagicMock
from gerrychain_queue.queue import Queue, repair_histogram


@pytest.fixture
def queue():
    Redis = MagicMock()
    Task = MagicMock()
    return Queue(dict(), key="queue", Cache=Redis, Task=Task)


def test_list_of_runs_includes_statuses(queue):
    list_of_runs = queue.list_tasks()
    assert all("status" in run.keys() for run in list_of_runs)


def test_repair_histogram():
    histogram = [
        [[0.19340000000000002, 0.1935], 482],
        [[0.1934, 0.19350000002], 200],
        [[0.1933, 0.19340000000000002], 537],
    ]
    repaired = repair_histogram(histogram)
    assert repaired == [((0.1934, 0.1935), 682), ((0.1933, 0.1934), 537)]
