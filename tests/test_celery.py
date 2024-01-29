from dataclasses import dataclass

import pytest
from celery import Celery

from src.analyzer import ECGAnalyzer, BackendChallengeECGAnalyzer
from src.celery.main import celery_app
from src.celery.tasks import async_count_zero_crosses


@pytest.fixture(scope='module')
def mocked_celery_app(request):
    celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery_app


@dataclass
class SignalResult:
    zero_crosses_counts: list[int]
    expected_count: int


@pytest.fixture
def mocked_zero_crosses() -> list[SignalResult]:
    return [
        SignalResult(zero_crosses_counts=[0, 1, 4, 0, 0, 13],
                     expected_count=18),
        SignalResult(zero_crosses_counts=[0, 0, 0, 1, 4, 5],
                     expected_count=10),
        SignalResult(zero_crosses_counts=[5, 1, 5, 0, 0, 0],
                     expected_count=11),
        SignalResult(zero_crosses_counts=[1, 1, 2, 1, 0, 1],
                     expected_count=6),
        SignalResult(zero_crosses_counts=[0, 0, 0, 0, 0, 0],
                     expected_count=0)
    ]


class TestCeleryTasks:
    def test_async_analyze(self, mocked_celery_app: Celery,
                           analyzer: ECGAnalyzer = BackendChallengeECGAnalyzer()):
        assert isinstance(analyzer.analyze([1, -3, 5]), int)
        assert analyzer.analyze([1, -3, 5]) == 2

    def test_async_count_zero_crosses(self, mocked_celery_app: Celery,
                                      mocked_zero_crosses: list[SignalResult]):
        for result in mocked_zero_crosses:
            assert async_count_zero_crosses(result.zero_crosses_counts) == result.expected_count
