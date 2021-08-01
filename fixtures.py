from datetime import datetime

import pytest


@pytest.fixture
def time_tracker():
    # the start time of tests
    tick = datetime.now()
    # run tests
    yield
    # the end time of tests
    tock = datetime.now()
    diff = tock - tick
    print(f"\n runtime: {diff.total_seconds()}")
