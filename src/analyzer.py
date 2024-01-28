from abc import abstractmethod, ABC


class ECGAnalyzer(ABC):
    @abstractmethod
    def analyze(self, signals: list[int]) -> int:
        """ Interface to analyze an ECG by its signals. """


class BackendChallengeECGAnalyzer(ECGAnalyzer):
    def analyze(self, signals: list[int]) -> int:
        count = 0
        for index, signal in enumerate(signals):
            if index == 0:
                continue
            elif signals[index - 1] > 0 > signal:
                count += 1
            elif signals[index - 1] < 0 < signal:
                count += 1
        return count
