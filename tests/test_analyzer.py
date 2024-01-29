from src.analyzer import BackendChallengeECGAnalyzer, BackendChallengeECGAnalyzer2
import pytest
from dataclasses import dataclass


@dataclass
class SignalFixture:
    signal: list[int]
    zero_crosses_count: int


@pytest.fixture
def mocked_signals() -> list[SignalFixture]:
    return [SignalFixture(signal=[80, 101, -115, -88, 5, 105, 181, -80, -92, 89, -150, 63, -85, 41, 89],
                          zero_crosses_count=8),
            SignalFixture(signal=[0, -3, -1, 7, -1, 0, 45],
                          zero_crosses_count=2),
            SignalFixture(signal=[23, -2, -5, -40, 1, 43, -2, 45, 45, 59, -20, 0, 2, -18],
                          zero_crosses_count=6),
            SignalFixture(signal=[5, 0, -4, 23, -9],
                          zero_crosses_count=2),
            SignalFixture(signal=[72, 53, 23, -1, -4, -2, 9, 75, 1, 0, -1, 4, 43, -23, -1, 2],
                          zero_crosses_count=5),
            SignalFixture(signal=[-1, -4, -1, -3, -10, -12, -45, -45, -59, -59],
                          zero_crosses_count=0),
            SignalFixture(signal=[42, -2, 23, -11, 3, -4, 45, -59, 68, 1, -1],
                          zero_crosses_count=9)
            ]


class TestECGAnalyzer:
    def test_ecg_analyzer(self, mocked_signals: list[SignalFixture]):
        analyzer = BackendChallengeECGAnalyzer()
        for signal_fixture in mocked_signals:
            assert analyzer.analyze(signal_fixture.signal) == signal_fixture.zero_crosses_count

    def test_ecg_analyzer2(self, mocked_signals: list[SignalFixture]):
        analyzer = BackendChallengeECGAnalyzer2()
        for signal_fixture in mocked_signals:
            assert analyzer.analyze(signal_fixture.signal) == signal_fixture.zero_crosses_count
