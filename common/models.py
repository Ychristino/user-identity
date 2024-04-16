from enum import Enum


class Models(Enum):
    ADABOOST = {'label': 'Adaboost',
                'value': 'adb',
                'id': 1
                }
    DECISION_TREE = {'label': 'Decision Tree',
                     'value': 'dt',
                     'id': 2
                     }
    RANDOM_FOREST = {'label': 'Random Forest',
                     'value': 'rf',
                     'id': 3
                     }
    GRADIENTBOOST = {'label': 'Gradient Boost',
                     'value': 'gb',
                     'id': 4
                     }
    KNEIGHBORS = {'label': 'KNeighbors',
                  'value': 'kn',
                  'id': 5
                  }
    LOGISTIC_REGRESSION = {'label': 'Logistic Regression',
                           'value': 'lr',
                           'id': 6
                           }
    SUPPORT_VECTOR_CLASSIFIER = {'label': 'Support Vector Classifier (SVC)',
                                 'value': 'svc',
                                 'id': 7
                                 }
    DUMMY_CLASSIFIER = {'label': 'Dummy (Metrics Only)',
                        'value': 'dum',
                        'id': 8
                        }


def find_model_by_value(value):
    for model in Models:
        if model.value['value'] == value:
            return model
    return None
