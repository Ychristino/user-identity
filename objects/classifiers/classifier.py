import os

import pandas as pd

from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

from abc import ABC, abstractmethod
from objects.analyses.mouse_analyses import MouseAnalyses
from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.analyses.keyboard_analyses import read_file as read_keyboard_file
from objects.analyses.mouse_analyses import read_file as read_mouse_file


def metrics(train_data: pd.DataFrame, test_data: pd.DataFrame, expected_train_predictions: pd.Series,
            expected_test_predictions: pd.Series, current_predictions: pd.Series):
    print(classification_report(expected_test_predictions, current_predictions, zero_division=0))
    print(f"Número de dados de treinamento: {len(train_data)}")
    print(f"Número de dados de teste: {len(test_data)}")

    print('Dados de treino:')
    print(expected_train_predictions.value_counts())
    print('Dados de Execução:')
    print(expected_test_predictions.value_counts())

    return precision_recall_fscore_support(expected_test_predictions, current_predictions, zero_division=0)


class Classifier(ABC):
    def __init__(self,
                 mouse_stats: pd.DataFrame = pd.DataFrame(),
                 keyboard_stats: pd.DataFrame = pd.DataFrame(),
                 mouse_analyses: MouseAnalyses = MouseAnalyses(),
                 keyboard_analyses: KeyboardAnalyses = KeyboardAnalyses()
                 ):

        self.df_mouse_stats = mouse_stats
        self.df_keyboard_stats = keyboard_stats

        self.mouse_analyses = mouse_analyses
        self.keyboard_analyses = keyboard_analyses

        self.classifier = None

    def load_mouse_analyses(self,
                            mouse_file_path: str,
                            identifier_label: str):
        list_mouse_movement_data, list_mouse_click_data = read_mouse_file(mouse_file_path)

        for index in range(len(list_mouse_movement_data)):
            self.mouse_analyses.mouse_movement_data = list_mouse_movement_data[index]
            self.mouse_analyses.extract_velocity_metrics(make_mean=False)
            self.mouse_analyses.extract_movement_metrics(make_mean=False)
            self.mouse_analyses.extract_distance_metrics(make_mean=False)

            if len(list_mouse_movement_data) > index:
                self.mouse_analyses.mouse_click_data = list_mouse_click_data[index]
                self.mouse_analyses.extract_clicks_metrics(make_mean=False)

            new_df = self.mouse_analyses.generate_dataframe()
            new_df['expected'] = identifier_label
            # VELOCIDADE | MOVIMENTACAO | DISTANCIA | CLICKS | DURACAO DOS CLICKS
            self.df_mouse_stats = self.df_mouse_stats._append(new_df, ignore_index=True)

    def load_keyboard_analyses(self,
                               keyboard_file_path: str,
                               identifier_label: str):
        list_keyboard_press_data, list_keyboard_release_data = read_keyboard_file(keyboard_file_path)
        for index in range(len(list_keyboard_press_data)):
            self.keyboard_analyses.keyboard_press_data = list_keyboard_press_data[index]
            self.keyboard_analyses.keyboard_release_data = list_keyboard_release_data[index]
            self.keyboard_analyses.extract_keyboard_data(make_mean=False)

            new_df = self.keyboard_analyses.generate_dataframe()
            new_df['expected'] = identifier_label

            self.df_keyboard_stats = self.df_keyboard_stats._append(new_df, ignore_index=True)

    def prepare_data(self,
                     validation_column_label: str = 'expected',
                     test_size: float = 0.2,
                     random_state: int = 42):

        x = self.df_mouse_stats.drop(validation_column_label, axis=1)
        y = self.df_mouse_stats[validation_column_label]

        x = x.fillna(0)
        y = y.fillna('guest')

        return train_test_split(x, y, test_size=test_size, random_state=random_state, stratify=y)

    @abstractmethod
    def create_classifier(self):
        raise Exception('This method should be implemented to run!')

    def execute_train(self, data_to_train, expected_value):
        self.classifier.fit(data_to_train, expected_value)

    def run_prediction(self, data_to_predict):
        return self.classifier.predict(data_to_predict)

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


if __name__ == '__main__':
    raise Exception('This class is not executable...')
