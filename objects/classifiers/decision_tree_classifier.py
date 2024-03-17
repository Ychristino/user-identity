import os
import pandas as pd

import matplotlib.pyplot as plt
from sklearn import tree

from sklearn.tree import DecisionTreeClassifier, plot_tree

from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.analyses.mouse_analyses import MouseAnalyses
from objects.classifiers.classifier import Classifier, metrics


class TreeClassifier(Classifier):

    def __init__(self,
                 mouse_stats: pd.DataFrame = pd.DataFrame(),
                 keyboard_stats: pd.DataFrame = pd.DataFrame(),
                 mouse_analyses: MouseAnalyses = MouseAnalyses(),
                 keyboard_analyses: KeyboardAnalyses = KeyboardAnalyses()
                 ):
        super().__init__(mouse_stats, keyboard_stats, mouse_analyses, keyboard_analyses)

    def create_classifier(self):
        self.classifier = DecisionTreeClassifier()

    def execute(self, base_directory: str = './files'):

        labels_executed = []
        for root, subdirectory, files in os.walk(base_directory):
            for folder in subdirectory:
                self.load_mouse_analyses(mouse_file_path=os.path.join(root, folder, 'mouse_data.json'),
                                         identifier_label=folder)
                self.load_keyboard_analyses(keyboard_file_path=os.path.join(root, folder, 'keyboard_data.json'),
                                            identifier_label=folder)
                labels_executed.append(labels_executed)

        x_train, x_test, y_train, y_test = self.prepare_data(validation_column_label='expected')
        self.create_classifier()

        self.execute_train(data_to_train=x_train, expected_value=y_train)
        predictions = self.run_prediction(data_to_predict=x_test)

        precision, recall, fscore, support = metrics(train_data=x_train,
                                                     test_data=x_test,
                                                     expected_train_predictions=y_train,
                                                     expected_test_predictions=y_test,
                                                     current_predictions=predictions)

        plt.figure(figsize=(10, 10))  # Ajuste o tamanho da figura conforme necessário
        plot_tree(self.classifier, filled=True, feature_names=self.df_mouse_stats.drop('expected', axis=1).columns,
                  class_names=True)
        plt.show()


if __name__ == '__main__':
    classifier = TreeClassifier()
    classifier.execute(base_directory='..\\..\\files')
