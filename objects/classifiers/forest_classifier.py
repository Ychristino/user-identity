import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_fscore_support

from objects.analyses.mouse_analyses import MouseAnalyses
from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.classifiers.classifier import Classifier


class ForesClassifier(Classifier):

    def __init__(self,
                 mouse_stats: pd.DataFrame = pd.DataFrame(),
                 keyboard_stats: pd.DataFrame = pd.DataFrame(),
                 mouse_analyses: MouseAnalyses = MouseAnalyses(),
                 keyboard_analyses: KeyboardAnalyses = KeyboardAnalyses()
                 ):
        super().__init__(mouse_stats, keyboard_stats, mouse_analyses, keyboard_analyses)

    def create_classifier(self, n_estimators: int = 100, random_state: int = 42):
        self.classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)


if __name__ == '__main__':
    classifier = ForesClassifier()

    # for root, subdirectory, files in os.walk('..\\..\\files'):
    #     for folder in subdirectory:
    #         classifier.load_mouse_analyses(mouse_file_path=os.path.join(root, folder, 'mouse_data.json'),
    #                                  identifier_label=folder)
    #         classifier.load_keyboard_analyses(keyboard_file_path=os.path.join(root, folder, 'keyboard_data.json'),
    #                                     identifier_label=folder)
    #
    # x_train, x_test, y_train, y_test = classifier.prepare_data(validation_column_label='expected')
    # classifier.create_classifier()
    #
    # classifier.execute_train(data_to_train=x_train, expected_value=y_train)
    # predictions = classifier.run_prediction(data_to_predict=x_test)
    #
    # print(classification_report(y_test, predictions, zero_division=0))
    # precision, recall, fscore, support = precision_recall_fscore_support(y_test, predictions, zero_division=0)
    # print(precision)
    # print(recall)
    # print(fscore)
    # print(support)
    # print(f"Número de dados de treinamento: {len(x_train)}")
    # print(f"Número de dados de teste: {len(x_test)}")
    #
    # print('Dados de treino:')
    # print(y_train.value_counts())
    # print('Dados de Execução:')
    # print(y_test.value_counts())

    classifier.execute(base_directory='..\\..\\files')
