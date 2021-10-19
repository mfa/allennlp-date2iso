from typing import Dict, List, Optional

from allennlp.training.metrics.metric import Metric
from overrides import overrides


@Metric.register("my_metrics")
class MyMetric(Metric):
    """
    This adds a sequence_accuracy metric counting all correct tokens in %
    """

    def __init__(self):
        self._num_same_sequence = 0
        self._num_all_sequences = 0

    @overrides
    def __call__(self, predictions, targets) -> None:
        for prediction, target in zip(predictions, targets):
            correct = sum([p == t for p, t in zip(prediction, target)])
            self._num_same_sequence += float(correct) / len(prediction)
            self._num_all_sequences += 1

    @overrides
    def get_metric(self, reset: bool = False) -> Dict[str, float]:
        if self._num_all_sequences == 0:
            metrics = {
                "sequence_accuracy": 0.0,
            }
        else:
            metrics = {
                "sequence_accuracy": self._num_same_sequence / self._num_all_sequences,
            }
        if reset:
            self.reset()
        return metrics

    @overrides
    def reset(self):
        self._num_same_sequence = 0
        self._num_all_sequences = 0
