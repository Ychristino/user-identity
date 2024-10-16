import os

import numpy as np
import pandas as pd

from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

from abc import ABC, abstractmethod

from sklearn.preprocessing import StandardScaler

from common.activity import Activity
from common.constants import MOUSE_FILE, KEYBOARD_FILE, BASE_DIR
from objects.analyses.mouse_analyses import MouseAnalyses
from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.analyses.keyboard_analyses import read_file as read_keyboard_file
from objects.analyses.mouse_analyses import read_file as read_mouse_file


def metrics(train_data: pd.DataFrame,
            test_data: pd.DataFrame,
            expected_train_predictions: pd.Series,
            expected_test_predictions: pd.Series,
            current_predictions: pd.Series,
            label_executed: tuple
            ):

    train_data_size = len(train_data)
    test_data_size = len(test_data)
    train_data = expected_train_predictions.value_counts()
    test_data = expected_test_predictions.value_counts()
    precision, recall, fscore, support = precision_recall_fscore_support(expected_test_predictions, current_predictions, zero_division=0)

    metrics_by_class = {}
    for i, class_label in enumerate(label_executed):
        metrics_by_class[class_label] = {
            'precision': float(precision[i]),
            'recall': float(recall[i]),
            'fscore': float(fscore[i]),
            'support': int(support[i])
        }

    return train_data_size, test_data_size, train_data, test_data, metrics_by_class


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
                            identifier_label: str,
                            merge_control: int,
                            activity: Activity = None
                            ):
        list_mouse_movement_data, list_mouse_click_data = read_mouse_file(mouse_file_path=mouse_file_path, activity=activity, split_data_every_n_seconds=15)

        for index in range(len(list_mouse_movement_data)):
            self.mouse_analyses.mouse_movement_data = list_mouse_movement_data[index]
            self.mouse_analyses.extract_velocity_metrics(make_mean=False)
            self.mouse_analyses.extract_movement_metrics(make_mean=False)
            self.mouse_analyses.extract_distance_metrics(make_mean=False)

            if index < len(list_mouse_click_data):
                self.mouse_analyses.mouse_click_data = list_mouse_click_data[index]
                self.mouse_analyses.extract_clicks_metrics(make_mean=False)

            self.mouse_analyses.extract_general_metrics(make_mean=False)

            new_df = self.mouse_analyses.generate_dataframe()
            new_df['expected'] = identifier_label

            if merge_control is not None:
                new_df['merge_control'] = merge_control

            # VELOCIDADE | MOVIMENTACAO | DISTANCIA | CLICKS | DURACAO DOS CLICKS
            self.df_mouse_stats = self.df_mouse_stats._append(new_df, ignore_index=True)

        return self.df_mouse_stats

    def load_keyboard_analyses(self,
                               keyboard_file_path: str,
                               identifier_label: str,
                               merge_control: int,
                               activity: Activity = None
                               ):
        list_keyboard_press_data, list_keyboard_release_data = read_keyboard_file(keyboard_file_path, activity=activity, split_data_every_n_seconds=15)
        for index in range(len(list_keyboard_press_data)):
            if len(list_keyboard_release_data) > index:
                self.keyboard_analyses.keyboard_press_data = list_keyboard_press_data[index]
                self.keyboard_analyses.keyboard_release_data = list_keyboard_release_data[index]
                self.keyboard_analyses.extract_keyboard_data(make_mean=False)

                new_df = self.keyboard_analyses.generate_dataframe()
                new_df['expected'] = identifier_label

                if merge_control is not None:
                    new_df['merge_control'] = merge_control

                self.df_keyboard_stats = self.df_keyboard_stats._append(new_df, ignore_index=True)

        return self.df_keyboard_stats

    def pre_processor(self, train_x: pd.DataFrame, test_x: pd.DataFrame):
        scaler = StandardScaler()
        scaler.fit(train_x)

        train_x = scaler.transform(train_x)
        test_x = scaler.transform(test_x)

        return train_x, test_x

    def prepare_data(self,
                     validation_column_label: str = 'expected',
                     test_size: float = 0.2,
                     random_state: int = 42,
                     use_mouse_data: bool = True,
                     use_keyboard_data: bool = True,
                     fill_na_values: bool = True,
                     filter_one_member_only: bool = False,
                     require_both: bool = True):

        if use_mouse_data and use_keyboard_data:
            assert ('merge_control' in self.df_mouse_stats or self.df_mouse_stats.emptyf) and ('merge_control' in self.df_keyboard_stats or self.df_keyboard_stats.empty)


        combined_data = pd.DataFrame()
        if use_mouse_data and not self.df_mouse_stats.empty:
            combined_data = self.df_mouse_stats.copy()
        elif not require_both:
            combined_data = pd.DataFrame(
                columns=self.df_keyboard_stats.columns)  # Cria um DataFrame vazio com as colunas do df_keyboard_stats

        if use_keyboard_data and not self.df_keyboard_stats.empty:
            if combined_data.empty:
                combined_data = self.df_keyboard_stats.copy()
            else:
                combined_data = pd.merge(combined_data, self.df_keyboard_stats, on=['merge_control', 'expected'],
                                         how='outer')
        elif not require_both:
            if combined_data.empty:
                combined_data = pd.DataFrame(
                    columns=self.df_mouse_stats.columns)  # Cria um DataFrame vazio com as colunas do df_mouse_stats
                missing_columns = [col for col in self.df_keyboard_stats.columns if col not in combined_data.columns]
                for col in missing_columns:
                    combined_data[col] = 0  # Fill missing columns with zeros

        combined_data = combined_data.drop(['merge_control'], axis=1)

        x = combined_data.drop(validation_column_label, axis=1)
        y = combined_data[validation_column_label]

        if fill_na_values:
            x = x.fillna(0)
            y = y.fillna('guest')

        if filter_one_member_only:
            # Contagem de ocorrências de cada classe
            unique_classes, class_counts = np.unique(y, return_counts=True)

            # Encontre as classes que têm apenas um registro
            single_instance_classes = unique_classes[class_counts == 1]

            # Remova as classes com apenas um membro do conjunto de dados
            combined_data = combined_data[~combined_data[validation_column_label].isin(single_instance_classes)]
            x = combined_data.drop(validation_column_label, axis=1)
            y = combined_data[validation_column_label]

        raw_x_train, raw_x_test, y_train, y_test = train_test_split(x, y, test_size=test_size,
                                                                    random_state=random_state,
                                                                    stratify=y)

        return raw_x_train, raw_x_test, y_train, y_test

    @abstractmethod
    def create_classifier(self):
        raise Exception('This method should be implemented to run!')

    def execute_train(self, data_to_train, expected_value):
        self.classifier.fit(data_to_train, expected_value)

    def run_prediction(self, data_to_predict):
        return self.classifier.predict(data_to_predict)

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
                                                                                           label_executed=tuple(labels_executed)
                                                                                           )

        return train_data_size, test_data_size, train_data, test_data, metrics_by_class


if __name__ == '__main__':
    raise Exception('This class is not executable...')
