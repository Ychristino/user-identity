import json
from typing import Tuple, List, Any

import numpy as np
import pandas as pd
from pandas import DataFrame, Series


def read_file(keyboard_file_path: str) -> tuple[list[DataFrame], list[DataFrame]]:
    """
    Realiza a leitura dos arquivos gravados de eventos do teclado, transformando-os em Dataframes para execução das
    leituras necessárias.
    :param keyboard_file_path: Caminho do arquivo de dados do teclado
    :return: Lista de Dataframes de eventos 'press' do teclado, Lista de Dataframes de eventos 'release' do teclado
    """
    with open(keyboard_file_path, 'r') as f:
        keyboard_data_json = json.load(f)

    list_df_keyboard_press_data = []
    list_df_keyboard_release_data = []

    for item in keyboard_data_json:
        if bool(item):
            df_keyboard_press_data = pd.DataFrame(item['press'])
            df_keyboard_release_data = pd.DataFrame(item['release'])

            if df_keyboard_press_data.empty or df_keyboard_release_data.empty:
                continue

            list_df_keyboard_press_data.append(df_keyboard_press_data)
            list_df_keyboard_release_data.append(df_keyboard_release_data)

    return list_df_keyboard_press_data, list_df_keyboard_release_data


class KeyboardAnalyses:
    """
    Classe responsável por ler os dados de teclado e realizar a extração e cálculos dos dados necessários.
    """
    def __init__(self, keyboard_press_data: pd.DataFrame = None, keyboard_release_data: pd.DataFrame = None):
        self.keyboard_press_data = keyboard_press_data
        self.keyboard_release_data = keyboard_release_data
        self.total_keys_pressed = None
        self.typing_ratio = None
        self.average_time_pressed = None
        self.average_interval_between_keys = None

    def extract_keyboard_data(self,
                              keyboard_pressed_data: pd.DataFrame = None,
                              keyboard_released_data: pd.DataFrame = None) -> list[int | float | Any] | None:
        """
        Realiza a extração dos dados e métricas do teclado, como velocidade de digitação, número de teclas
        pressionadas, etc.
        :param keyboard_pressed_data: Dataframe de dados de evento 'press' do teclado
        :param keyboard_released_data: Dataframe de dados de evento 'release' do teclado
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if keyboard_pressed_data is not None:
            df_keys_pressed = keyboard_pressed_data
        else:
            df_keys_pressed = self.keyboard_press_data

        if keyboard_released_data is not None:
            df_keys_released = keyboard_released_data
        else:
            df_keys_released = self.keyboard_release_data

        df_keys_pressed = df_keys_pressed[['key', 'time']]
        df_keys_released = df_keys_released[['key', 'time']]

        total_keys_pressed = len(df_keys_pressed)
        self.total_keys_pressed = np.nanmean([self.total_keys_pressed,
                                              total_keys_pressed]) if self.total_keys_pressed is not None else total_keys_pressed

        # typing_ratio
        total_typing_time_seconds = df_keys_released['time'].max() - df_keys_pressed['time'].min()
        typing_ratio = total_keys_pressed / total_typing_time_seconds
        self.typing_ratio = np.nanmean(
            [self.typing_ratio, typing_ratio]) if self.typing_ratio is not None else typing_ratio

        # average_time_pressed
        merged = pd.merge(df_keys_pressed, df_keys_released, on='key', suffixes=('_press', '_release'))
        merged['time_pressed'] = merged['time_release'] - merged['time_press']
        average_time_pressed = merged['time_pressed'].mean()
        self.average_time_pressed = np.nanmean([self.average_time_pressed,
                                                average_time_pressed]) if self.average_time_pressed is not None else average_time_pressed

        # average_interval_between_keys
        df_keys_pressed['time_next_key'] = df_keys_pressed['time'].shift(-1)
        df_keys_pressed['interval_to_next_key'] = df_keys_pressed['time_next_key'] - df_keys_pressed['time']
        average_interval_between_keys = df_keys_pressed['interval_to_next_key'].mean()
        self.average_interval_between_keys = np.nanmean([self.average_interval_between_keys,
                                                         average_interval_between_keys]) if self.average_interval_between_keys is not None else average_interval_between_keys

        return [self.total_keys_pressed, self.typing_ratio, self.average_time_pressed,
                self.average_interval_between_keys]


if __name__ == '__main__':
    analyses = KeyboardAnalyses()
    list_keyboard_press_data, list_keyboard_release_data = read_file('../../files/user/keyboard_data.json')

    for index in range(len(list_keyboard_press_data)):
        analyses.keyboard_press_data = list_keyboard_press_data[index]

        analyses.keyboard_release_data = list_keyboard_release_data[index]

        analyses.extract_keyboard_data()
