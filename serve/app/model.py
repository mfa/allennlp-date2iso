import allennlp
import my_metrics
from allennlp.models.archival import load_archive
from allennlp.predictors.predictor import Predictor


def get_predictor():
    allennlp.common.plugins.import_plugins()

    archive = load_archive("model.tar.gz")
    predictor = Predictor.from_archive(archive)
    predictor.version = "2021-10-14"
    return predictor
