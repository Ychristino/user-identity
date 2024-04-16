import os
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier, plot_tree

from common.activity import Activity
from common.constants import MOUSE_FILE, KEYBOARD_FILE, BASE_DIR
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

    def execute(self,
                base_directory: str = os.path.join(BASE_DIR, 'files'),
                activity: Activity = None
                ):
        labels_executed = []
        merge_control = 0

        for subdirectory in os.listdir(base_directory):
            merge_control += 1
            self.load_mouse_analyses(mouse_file_path=os.path.join(base_directory, subdirectory),
                                     identifier_label=subdirectory,
                                     merge_control=merge_control,
                                     activity=activity
                                     )
            self.load_keyboard_analyses(keyboard_file_path=os.path.join(base_directory, subdirectory),
                                        identifier_label=subdirectory,
                                        merge_control=merge_control,
                                        activity=activity
                                        )
            if subdirectory in self.df_mouse_stats['expected'].values and subdirectory in self.df_keyboard_stats['expected'].values:
                labels_executed.append(subdirectory)

        raw_x_train, raw_x_test, y_train, y_test = self.prepare_data(validation_column_label='expected',
                                                                     filter_one_member_only=True)

        x_train, x_test = self.pre_processor(raw_x_train, raw_x_test)

        self.create_classifier()

        self.execute_train(data_to_train=x_train, expected_value=y_train)
        predictions = self.run_prediction(data_to_predict=x_test)

        train_data_size, test_data_size, train_data, test_data, metrics_by_class = metrics(train_data=x_train,
                                                                                           test_data=x_test,
                                                                                           expected_train_predictions=y_train,
                                                                                           expected_test_predictions=y_test,
                                                                                           current_predictions=predictions,
                                                                                           label_executed=tuple(
                                                                                               labels_executed)
                                                                                           )

        plt.figure(figsize=(10, 10))  # Ajuste o tamanho da figura conforme necessário
        plot_tree(self.classifier,
                  filled=True,
                  feature_names=raw_x_train.columns,
                  class_names=labels_executed,
                  max_depth=5)
        plt.show()

        return train_data_size, test_data_size, train_data, test_data, metrics_by_class


if __name__ == '__main__':
    classifier = TreeClassifier()
    classifier.execute(base_directory=os.path.join('../../', 'files'))
