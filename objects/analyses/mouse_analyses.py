import os
from typing import Any

import numpy as np
import pandas as pd
import json

from pandas import DataFrame
from pynput.mouse import Button

from common.click_status import ClickStatus
from common.constants import MOUSE_FILE, BASE_DIR


def read_file(mouse_file_path: str) -> tuple[list[DataFrame], list[DataFrame]]:
    """
    Realiza a leitura dos arquivos gravados de eventos do mouse, transformando-os em Dataframes para execução das
    leituras necessárias.
    :param mouse_file_path: Caminho do arquivo de dados do mouse
    :return: Lista de Dataframes de eventos 'move' do mouse, Lista de Dataframes de eventos 'click' do mouse
    """
    with open(mouse_file_path, 'r') as f:
        mouse_data_json = json.load(f)

    list_df_mouse_movement_data = []
    list_df_mouse_click_data = []

    for item in mouse_data_json:

        if bool(item):
            df_mouse_movement_data = pd.DataFrame(item['move'])
            df_mouse_click_data = pd.DataFrame(item['click'])

            if not df_mouse_movement_data.empty:
                list_df_mouse_movement_data.append(df_mouse_movement_data)

            if not df_mouse_click_data.empty:
                list_df_mouse_click_data.append(df_mouse_click_data)

    return list_df_mouse_movement_data, list_df_mouse_click_data


class MouseAnalyses:
    """
    Classe responsável por ler os dados de mouse e realizar a extração e cálculos dos dados necessários.
    """

    def __init__(self, mouse_movement_data: pd.DataFrame = None, mouse_click_data: pd.DataFrame = None):

        # DADOS PADRÃO, NECESSÁRIOS PARA REALIZAR A EXTRACAO DOS DADOS
        self.mouse_movement_data = mouse_movement_data
        self.mouse_click_data = mouse_click_data

        # VELOCIDADE
        self.up_average_speed = None
        self.down_average_speed = None
        self.right_average_speed = None
        self.left_average_speed = None

        self.vertical_average_speed = None
        self.horizontal_average_speed = None
        self.average_speed = None

        self.maximum_horizontal_speed = None
        self.maximum_vertical_speed = None
        self.minimum_horizontal_speed = None
        self.minimum_vertical_speed = None
        self.maximum_speed = None
        self.minimum_speed = None

        # MOVIMENTACAO
        self.up_moves = None
        self.down_moves = None
        self.left_moves = None
        self.right_moves = None

        self.horizontal_moves = None
        self.vertical_moves = None

        # DISTANCIAS
        self.up_distance = None
        self.down_distance = None
        self.left_distance = None
        self.right_distance = None

        self.horizontal_distance = None
        self.vertical_distance = None
        self.total_distance = None

        # CLICKS
        self.total_clicks = None
        self.right_clicks = None
        self.left_clicks = None

        # DURACAO DOS CLICKS
        self.right_click_total_duration = None
        self.left_click_total_duration = None

        self.right_click_average_duration = None
        self.left_click_average_duration = None

        # STOP
        self.non_movement_time = None
        self.non_clicks_time = None
        self.non_action_time = None

    def extract_velocity_metrics(self, mouse_movement_data: pd.DataFrame = None, make_mean: bool = True) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, como velocidade de movimentação, velocidade mínima e máxima dos movimento, etc.
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
        :param make_mean: Se já existir um valor anterior gravado, calcula a média entre o atual e o anterior
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_movement_data is not None:
            df_velocity = mouse_movement_data
        else:
            df_velocity = self.mouse_movement_data[['x_position', 'y_position', 'time']]

        # Calculando as variações de posição em relação ao tempo para cada direção
        df_velocity['x_variation'] = df_velocity['x_position'].diff()
        df_velocity['y_variation'] = df_velocity['y_position'].diff()
        df_velocity['time_variation'] = df_velocity['time'].diff()
        df_velocity = df_velocity.fillna(0)

        # Calculando as velocidades médias em cada direção
        up_average_speed = df_velocity[df_velocity['y_variation'] < 0]['y_variation'].sum() / df_velocity[
            'time_variation'].sum()
        self.up_average_speed = np.nanmean([self.up_average_speed, up_average_speed]) if (
                self.up_average_speed is not None and make_mean) else up_average_speed if not np.isnan(
            up_average_speed) else 0

        down_average_speed = df_velocity[df_velocity['y_variation'] > 0]['y_variation'].sum() / df_velocity[
            'time_variation'].sum()
        self.down_average_speed = np.nanmean([self.down_average_speed, down_average_speed]) if (
                self.down_average_speed is not None and make_mean) else down_average_speed if not np.isnan(
            down_average_speed) else 0

        right_average_speed = df_velocity[df_velocity['x_variation'] > 0]['x_variation'].sum() / df_velocity[
            'time_variation'].sum()
        self.right_average_speed = np.nanmean([self.right_average_speed, right_average_speed]) if (
                self.right_average_speed is not None and make_mean) else right_average_speed if not np.isnan(
            right_average_speed) else 0

        left_average_speed = df_velocity[df_velocity['x_variation'] < 0]['x_variation'].sum() / df_velocity[
            'time_variation'].sum()
        self.left_average_speed = np.nanmean([self.left_average_speed, up_average_speed]) if (
                self.left_average_speed is not None and make_mean) else left_average_speed if not np.isnan(
            left_average_speed) else 0

        # Calculando velocidade média vertical e horizontal
        vertical_average_speed = (self.up_average_speed + abs(self.down_average_speed)) / 2
        self.vertical_average_speed = np.nanmean([self.vertical_average_speed, vertical_average_speed]) if (
                self.vertical_average_speed is not None and make_mean) else vertical_average_speed if not np.isnan(
            vertical_average_speed) else 0

        horizontal_average_speed = (self.right_average_speed + abs(self.left_average_speed)) / 2
        self.horizontal_average_speed = np.nanmean([self.horizontal_average_speed, horizontal_average_speed]) if (
                self.horizontal_average_speed is not None and make_mean) else horizontal_average_speed if not np.isnan(
            horizontal_average_speed) else 0

        # Calculando a velocidade média total
        average_speed = (abs(self.up_average_speed) + abs(self.down_average_speed) + abs(
            self.right_average_speed) + abs(self.left_average_speed)) / 4
        self.average_speed = np.nanmean([self.average_speed, average_speed]) if (
                self.average_speed is not None and make_mean) else average_speed if not np.isnan(
            average_speed) else 0

        # Calculando as velocidades máximas e mínimas em cada direção
        maximum_horizontal_speed = max(self.right_average_speed, abs(self.left_average_speed))
        self.maximum_horizontal_speed = np.nanmean([self.maximum_horizontal_speed, maximum_horizontal_speed]) if (
                self.maximum_horizontal_speed is not None and make_mean) else maximum_horizontal_speed if not np.isnan(
            maximum_horizontal_speed) else 0

        minimum_horizontal_speed = min(self.right_average_speed, abs(self.left_average_speed))
        self.minimum_horizontal_speed = np.nanmean([self.minimum_horizontal_speed, minimum_horizontal_speed]) if (
                self.minimum_horizontal_speed is not None and make_mean) else minimum_horizontal_speed if not np.isnan(
            minimum_horizontal_speed) else 0

        maximum_vertical_speed = max(self.up_average_speed, abs(self.down_average_speed))
        self.maximum_vertical_speed = np.nanmean([self.maximum_vertical_speed, maximum_vertical_speed]) if (
                self.maximum_vertical_speed is not None and make_mean) else maximum_vertical_speed if not np.isnan(
            maximum_vertical_speed) else 0

        minimum_vertical_speed = min(self.up_average_speed, abs(self.down_average_speed))
        self.minimum_vertical_speed = np.nanmean([self.minimum_vertical_speed, minimum_vertical_speed]) if (
                self.minimum_vertical_speed is not None and make_mean) else minimum_vertical_speed if not np.isnan(
            minimum_vertical_speed) else 0

        # Calculando a velocidade máxima e mínima total
        maximum_speed = max(abs(self.up_average_speed), abs(self.down_average_speed),
                            abs(self.right_average_speed), abs(self.left_average_speed))
        self.maximum_speed = np.nanmean([self.maximum_speed, maximum_speed]) if (
                self.maximum_speed is not None and make_mean) else maximum_speed if not np.isnan(
            maximum_speed) else 0

        minimum_speed = min(abs(self.up_average_speed), abs(self.down_average_speed),
                            abs(self.right_average_speed), abs(self.left_average_speed))
        self.minimum_speed = np.nanmean([self.minimum_speed, minimum_speed]) if (
                self.minimum_speed is not None and make_mean) else minimum_speed if not np.isnan(
            minimum_speed) else 0

        return [self.up_average_speed, self.down_average_speed, self.right_average_speed, self.left_average_speed,
                self.vertical_average_speed, self.horizontal_average_speed, self.average_speed,
                self.maximum_horizontal_speed, self.minimum_horizontal_speed, self.maximum_vertical_speed,
                self.minimum_vertical_speed,
                self.maximum_speed, self.minimum_speed]

    def extract_movement_metrics(self, mouse_movement_data: pd.DataFrame = None, make_mean: bool = True) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, como quantidade de movimentos, direções, etc.
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
        :param make_mean: Se já existir um valor anterior gravado, calcula a média entre o atual e o anterior
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_movement_data is not None:
            df_movement = mouse_movement_data
        else:
            df_movement = self.mouse_movement_data[['x_position', 'y_position', 'time']]

        df_movement = df_movement[['x_position', 'y_position', 'time']]
        df_movement = df_movement.sort_values(by='time')

        # Calcular as mudanças de direção
        df_movement['mudanca_x'] = df_movement['x_position'].diff().apply(np.sign)
        df_movement['mudanca_y'] = df_movement['y_position'].diff().apply(np.sign)
        df_movement = df_movement.fillna(0)

        # Contar os movimentos
        up_moves = (df_movement['mudanca_y'] > 0).sum()
        self.up_moves = np.nanmean([self.up_moves, up_moves]) if (
                self.up_moves is not None and make_mean) else up_moves if not np.isnan(up_moves) else 0

        down_moves = (df_movement['mudanca_y'] < 0).sum()
        self.down_moves = np.nanmean([self.down_moves, down_moves]) if (
                self.down_moves is not None and make_mean) else down_moves if not np.isnan(down_moves) else 0

        right_moves = (df_movement['mudanca_x'] > 0).sum()
        self.right_moves = np.nanmean([self.right_moves, right_moves]) if (
                self.right_moves is not None and make_mean) else right_moves if not np.isnan(right_moves) else 0

        left_moves = (df_movement['mudanca_x'] < 0).sum()
        self.left_moves = np.nanmean([self.left_moves, left_moves]) if (
                self.left_moves is not None and make_mean) else left_moves if not np.isnan(left_moves) else 0

        horizontal_moves = self.right_moves + self.left_moves
        self.horizontal_moves = np.nanmean(
            [self.horizontal_moves, horizontal_moves]) if (
                self.horizontal_moves is not None and make_mean) else horizontal_moves if not np.isnan(
            horizontal_moves) else 0

        vertical_moves = self.up_moves + self.down_moves
        self.vertical_moves = np.nanmean(
            [self.vertical_moves, vertical_moves]) if (
                self.vertical_moves is not None and make_mean) else vertical_moves if not np.isnan(
            vertical_moves) else 0

        return [self.up_moves, self.down_moves, self.right_moves, self.left_moves, self.horizontal_moves,
                self.vertical_moves]

    def extract_distance_metrics(self, mouse_movement_data: pd.DataFrame = None, make_mean: bool = True) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, distância percorrida pelo ponteiro em cada direção.
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
        :param make_mean: Se já existir um valor anterior gravado, calcula a média entre o atual e o anterior
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_movement_data is not None:
            df_distance = mouse_movement_data
        else:
            df_distance = self.mouse_movement_data[['x_position', 'y_position', 'time']]

        df_distance = df_distance.sort_values(by='time')

        # Calcular a diferença entre pontos consecutivos
        df_distance['diff_x'] = df_distance['x_position'].diff()
        df_distance['diff_y'] = df_distance['y_position'].diff()
        df_distance = df_distance.fillna(0)

        # Calcular as distâncias
        horizontal_distance = df_distance['diff_x'].abs().sum()
        self.horizontal_distance = np.nanmean([self.horizontal_distance,
                                               horizontal_distance]) if (
                self.horizontal_distance is not None and make_mean) else horizontal_distance if not np.isnan(
            horizontal_distance) else 0

        vertical_distance = df_distance['diff_y'].abs().sum()
        self.vertical_distance = np.nanmean(
            [self.vertical_distance, vertical_distance]) if (
                self.vertical_distance is not None and make_mean) else vertical_distance if not np.isnan(
            vertical_distance) else 0

        total_distance = np.sqrt(df_distance['diff_x'] ** 2 + df_distance['diff_y'] ** 2).sum()
        self.total_distance = np.nanmean(
            [self.total_distance, total_distance]) if (
                self.total_distance is not None and make_mean) else total_distance if not np.isnan(
            total_distance) else 0

        # Calcular as distâncias para cima, para baixo, para a esquerda e para a direita
        up_distance = df_distance[df_distance['diff_y'] > 0]['diff_y'].sum()
        self.up_distance = np.nanmean([self.up_distance, up_distance]) if (
                self.up_distance is not None and make_mean) else up_distance if not np.isnan(up_distance) else 0

        down_distance = -df_distance[df_distance['diff_y'] < 0]['diff_y'].sum()
        self.down_distance = np.nanmean(
            [self.down_distance, down_distance]) if (
                self.down_distance is not None and make_mean) else down_distance if not np.isnan(
            down_distance) else 0

        right_distance = df_distance[df_distance['diff_x'] > 0]['diff_x'].sum()
        self.right_distance = np.nanmean(
            [self.right_distance, right_distance]) if (
                self.right_distance is not None and make_mean) else right_distance if not np.isnan(
            right_distance) else 0

        left_distance = -df_distance[df_distance['diff_x'] < 0]['diff_x'].sum()
        self.left_distance = np.nanmean(
            [self.left_distance, left_distance]) if (
                self.left_distance is not None and make_mean) else left_distance if not np.isnan(
            left_distance) else 0

        return [self.horizontal_distance, self.vertical_distance, self.total_distance, self.up_distance,
                self.down_distance, self.right_distance, self.left_distance]

    def extract_clicks_metrics(self, mouse_click_data: pd.DataFrame = None, make_mean: bool = True) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, clicks, velocidade de click, etc.
        :param mouse_click_data: Dataframe de dados de evento 'click' do mouse
        :param make_mean: Se já existir um valor anterior gravado, calcula a média entre o atual e o anterior
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_click_data is not None:
            df_clicks = mouse_click_data
        else:
            df_clicks = self.mouse_click_data[['x_position', 'y_position', 'button', 'status', 'time']]

        df_clicks = df_clicks.sort_values(by='time')

        # Calcular o número total de cliques
        total_clicks = df_clicks[df_clicks['status'] == ClickStatus.PRESS.value].shape[0]
        self.total_clicks = np.nanmean([self.total_clicks, total_clicks]) if (
                self.total_clicks is not None and make_mean) else total_clicks if not np.isnan(total_clicks) else 0

        # Calcular o número de cliques direitos e esquerdos
        right_clicks = df_clicks[
            (df_clicks['button'] == str(Button.right)) & (df_clicks['status'] == ClickStatus.PRESS.value)].shape[0]
        self.right_clicks = np.nanmean([self.right_clicks, right_clicks]) if (
                self.right_clicks is not None and make_mean) else right_clicks if not np.isnan(right_clicks) else 0

        left_clicks = df_clicks[
            (df_clicks['button'] == str(Button.left)) & (df_clicks['status'] == ClickStatus.PRESS.value)].shape[0]
        self.left_clicks = np.nanmean([self.left_clicks, left_clicks]) if (
                self.left_clicks is not None and make_mean) else left_clicks if not np.isnan(left_clicks) else 0

        click_pairs = pd.DataFrame(columns=['button', 'press_time', 'release_time'])

        # Encontra os pares 'press' e 'release' para o mesmo botão
        for button in [Button.right, Button.left]:
            press_times = \
                df_clicks[(df_clicks['button'] == str(button)) & (df_clicks['status'] == ClickStatus.PRESS.value)][
                    'time']
            release_times = \
                df_clicks[(df_clicks['button'] == str(button)) & (df_clicks['status'] == ClickStatus.RELEASE.value)][
                    'time']

            # Certificar que existe o mesmo número de eventos 'press' e 'release'
            if len(press_times) > len(release_times):
                press_times = press_times.iloc[:len(release_times)]
            elif len(release_times) > len(press_times):
                release_times = release_times.iloc[:len(press_times)]

            button_pairs = pd.DataFrame(
                {'button': str(button), 'press_time': press_times.values, 'release_time': release_times.values})

            if not button_pairs.empty:
                if click_pairs.empty:
                    click_pairs = button_pairs
                else:
                    click_pairs = pd.concat([click_pairs, button_pairs])

        # Calcula a duração de cada par de cliques
        click_pairs['duration'] = click_pairs['release_time'] - click_pairs['press_time']

        right_click_total_duration = click_pairs[click_pairs['button'] == str(Button.right)]['duration'].sum()
        self.right_click_total_duration = np.nanmean([self.right_click_total_duration, right_click_total_duration]) if (
                self.right_click_total_duration is not None and make_mean) else right_click_total_duration if not np.isnan(
            right_click_total_duration) else 0

        left_click_total_duration = click_pairs[click_pairs['button'] == str(Button.left)]['duration'].sum()
        self.left_click_total_duration = np.nanmean([self.left_click_total_duration, left_click_total_duration]) if (
                self.left_click_total_duration is not None and make_mean) else left_click_total_duration if not np.isnan(
            left_click_total_duration) else 0

        right_click_average_duration = click_pairs[click_pairs['button'] == str(Button.right)]['duration'].mean()
        self.right_click_average_duration = np.nanmean(
            [self.right_click_average_duration, right_click_average_duration]) if (
                self.right_click_average_duration is not None and make_mean) else right_click_average_duration if not np.isnan(
            right_click_average_duration) else 0

        left_click_average_duration = click_pairs[click_pairs['button'] == str(Button.left)]['duration'].mean()
        self.left_click_average_duration = np.nanmean(
            [self.left_click_average_duration, left_click_average_duration]) if (
                self.left_click_average_duration is not None and make_mean) else left_click_average_duration if not np.isnan(
            left_click_average_duration) else 0

        return [self.total_clicks, self.right_clicks, self.left_clicks, self.right_click_total_duration,
                self.left_click_total_duration, self.right_click_average_duration, self.left_click_average_duration]

    def extract_general_metrics(self, mouse_click_data: pd.DataFrame = None,
                                mouse_movement_data: pd.DataFrame = None,
                                make_mean: bool = True,
                                move_interval_tolerance: float = 0.1,
                                click_interval_tolerance: float = 0.1
                                ) -> list[Any]:
        """
        Realiza a extração dos dados e métricas gerais do mouse, como tempo sem movimentos, tempo sem click, etc.
        :param mouse_click_data: Dataframe de dados de evento 'click' do mouse
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
        :param make_mean: Se já existir um valor anterior gravado, calcula a média entre o atual e o anterior
        :param move_interval_tolerance: Tolerância em segundos entre os eventos, a fim de que seja considerado um movimento contínuo ou tempo ocioso
        :param click_interval_tolerance: Tolerância em segundos entre os eventos, a fim de que seja considerado um duplo click ou tempo ocioso
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_click_data is not None:
            df_clicks = mouse_click_data
        else:
            df_clicks = self.mouse_click_data[['x_position', 'y_position', 'button', 'status', 'time']]

        if mouse_movement_data is not None:
            df_movement = mouse_movement_data
        else:
            df_movement = self.mouse_movement_data[['x_position', 'y_position', 'time']]

        df_movement = df_movement.sort_values(by='time')
        df_clicks = df_clicks.sort_values(by='time')

        # Criando a coluna time_interval com valores nulos
        df_movement['time_interval'] = np.nan
        df_clicks['time_interval'] = np.nan

        df_movement['time_interval'] = df_movement['time'].diff()
        df_clicks['time_interval'] = df_clicks['time'].diff()

        # Replicando o tempo na coluna time_interval apenas na primeira linha
        if len(df_movement) > 0:
            df_movement.loc[df_movement.index[0], 'time_interval'] = df_movement.iloc[0]['time']
        if len(df_clicks) > 0:
            df_clicks.loc[df_clicks.index[0], 'time_interval'] = df_clicks.iloc[0]['time']

        df_non_movement = df_movement[df_movement['time_interval'] > move_interval_tolerance]
        df_non_clicks = df_clicks[df_clicks['time_interval'] > click_interval_tolerance]

        total_non_movement_time = df_non_movement['time_interval'].sum()
        self.non_movement_time = np.nanmean(
            [self.non_movement_time, total_non_movement_time]) if (
                self.non_movement_time is not None and make_mean) else total_non_movement_time if not np.isnan(
            total_non_movement_time) else 0

        total_non_clicks_time = df_non_clicks['time_interval'].sum()
        self.non_clicks_time = np.nanmean(
            [self.non_clicks_time, total_non_clicks_time]) if (
                self.non_clicks_time is not None and make_mean) else total_non_clicks_time if not np.isnan(
            total_non_clicks_time) else 0

        self.non_action_time = self.non_movement_time + self.non_clicks_time

        return [self.non_movement_time, self.non_clicks_time, self.non_action_time]

    def generate_dataframe(self):
        data = {
            'up_average_speed': self.up_average_speed,
            'down_average_speed': self.down_average_speed,
            'right_average_speed': self.right_average_speed,
            'left_average_speed': self.left_average_speed,
            'vertical_average_speed': self.vertical_average_speed,
            'horizontal_average_speed': self.horizontal_average_speed,
            'average_speed': self.average_speed,
            'maximum_horizontal_speed': self.maximum_horizontal_speed,
            'maximum_vertical_speed': self.maximum_vertical_speed,
            'minimum_horizontal_speed': self.minimum_horizontal_speed,
            'minimum_vertical_speed': self.minimum_vertical_speed,
            'maximum_speed': self.maximum_speed,
            'minimum_speed': self.minimum_speed,
            'up_moves': self.up_moves,
            'down_moves': self.down_moves,
            'left_moves': self.left_moves,
            'right_moves': self.right_moves,
            'horizontal_moves': self.horizontal_moves,
            'vertical_moves': self.vertical_moves,
            'up_distance': self.up_distance,
            'down_distance': self.down_moves,
            'left_distance': self.left_distance,
            'right_distance': self.right_distance,
            'horizontal_distance': self.horizontal_distance,
            'vertical_distance': self.vertical_distance,
            'total_distance': self.total_distance,
            'total_clicks': self.total_clicks,
            'right_clicks': self.right_distance,
            'left_clicks': self.left_distance,
            'right_click_total_duration': self.right_click_total_duration,
            'left_click_total_duration': self.left_click_total_duration,
            'right_click_average_duration': self.right_click_average_duration,
            'left_click_average_duration': self.left_click_average_duration,
            'non_movement_time': self.non_movement_time,
            'non_clicks_time': self.non_clicks_time,
            'non_action_time': self.non_action_time,
        }
        df_return = pd.DataFrame([data])
        return df_return.iloc[0]


if __name__ == '__main__':
    analyses = MouseAnalyses()
    list_mouse_movement_data, list_mouse_click_data = read_file(os.path.join('../../', 'files', 'user', MOUSE_FILE))

    for move_data in list_mouse_movement_data:
        analyses.mouse_movement_data = move_data

        analyses.extract_velocity_metrics()
        analyses.extract_movement_metrics()
        analyses.extract_distance_metrics()

    for click_data in list_mouse_click_data:
        analyses.mouse_click_data = click_data
        analyses.extract_clicks_metrics()

    print(analyses.generate_dataframe())
