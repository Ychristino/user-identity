import json
import os

from common.activity import Activity
from common.constants import BASE_DIR
from common.models import Models
from objects.classifiers.adaboost_classifier import AdaBoostClassifier
from objects.classifiers.decision_tree_classifier import TreeClassifier
from objects.classifiers.dummy_classifier import DummyClassifier
from objects.classifiers.forest_classifier import ForesClassifier
from objects.classifiers.gradientboost_classifier import GradientClassifier
from objects.classifiers.kneighbors_classifier import KneiborsClassifier
from objects.classifiers.logistic_regression import LogisticRegressionClassifier
from objects.classifiers.svc_classifier import SVCClassifier


class ModelService:

    def get_model_list(self):
        return_data = {'data': []}
        for model in Models:
            return_data['data'].append(model.value)
        return return_data

    def execute_model(self, model: Models, activity: Activity):
        selected_model = None

        match model:
            case Models.ADABOOST:
                selected_model = AdaBoostClassifier()
            case Models.DECISION_TREE:
                selected_model = TreeClassifier()
            case Models.RANDOM_FOREST:
                selected_model = ForesClassifier()
            case Models.GRADIENTBOOST:
                selected_model = GradientClassifier()
            case Models.KNEIGHBORS:
                selected_model = KneiborsClassifier()
            case Models.LOGISTIC_REGRESSION:
                selected_model = LogisticRegressionClassifier()
            case Models.SUPPORT_VECTOR_CLASSIFIER:
                selected_model = SVCClassifier()
            case Models.DUMMY_CLASSIFIER:
                selected_model = DummyClassifier()
            case _:
                raise Exception('Not a valid Model')

        train_data_size, test_data_size, train_data, test_data, metrics_by_class = selected_model.execute(base_directory=os.path.join(BASE_DIR, 'files'), activity=activity)

        return {
            'data': {
                'train_data_size': train_data_size,
                'test_data_size': test_data_size,
                'train_data': [{'user': index, 'quantity': value} for index, value in train_data.items()],
                'test_data': [{'user': index, 'quantity': value} for index, value in test_data.items()],
                'metrics_by_class': metrics_by_class,
            }
        }
