import pandas as pd
from sklearn.dummy import DummyClassifier as Dummy

from objects.analyses.mouse_analyses import MouseAnalyses
from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.classifiers.classifier import Classifier


class DummyClassifier(Classifier):

    def __init__(self,
                 mouse_stats: pd.DataFrame = pd.DataFrame(),
                 keyboard_stats: pd.DataFrame = pd.DataFrame(),
                 mouse_analyses: MouseAnalyses = MouseAnalyses(),
                 keyboard_analyses: KeyboardAnalyses = KeyboardAnalyses()
                 ):
        super().__init__(mouse_stats, keyboard_stats, mouse_analyses, keyboard_analyses)

    def create_classifier(self):
        self.classifier = Dummy(strategy='stratified')


if __name__ == '__main__':
    classifier = DummyClassifier()
    classifier.execute(base_directory='..\\..\\files')
