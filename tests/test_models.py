import pytest
from gerrychain_queue.runs import Run


def test_Run_can_be_instantiated_with_basic_run_spec(run_spec):
    run = Run(run_spec)
    assert run


def test_Run_requires_graph(run_spec):
    del run_spec["graph"]
    with pytest.raises(ValueError):
        Run(run_spec)


def test_Run_requires_constraints(run_spec):
    del run_spec["constraints"]
    with pytest.raises(ValueError):
        Run(run_spec)


def test_Run_requires_total_steps(run_spec):
    del run_spec["total_steps"]
    with pytest.raises(ValueError):
        Run(run_spec)
