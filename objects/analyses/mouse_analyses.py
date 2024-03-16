from typing import Tuple, List, Any

import numpy as np
import pandas as pd
import json

from pandas import DataFrame, Series
from pynput.mouse import Button

from common.click_status import ClickStatus


def read_file(mouse_file_path: str) -> tuple[list[DataFrame], list[DataFrame]]:
    """
    Realiza a leitura dos arquivos gravados de eventos do mouse, transformando-os em Dataframes para execução das
    leituras necessárias.
    :param mouse_file_path: Caminho do arquivo de dados do mouse
    :return: Lista de Dataframes de eventos 'move' do mouse, Lista de Dataframes de eventos 'click' do mouse
    """
    with open(mouse_file_path, 'r') as f:
        keyboard_data_json = json.load(f)

    list_df_mouse_movement_data = []
    list_df_mouse_click_data = []

    for item in keyboard_data_json:

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

    def extract_velocity_metrics(self, mouse_movement_data: pd.DataFrame = None) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, como velocidade de movimentação, velocidade mínima e máxima dos movimento, etc.
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_movement_data is not None:
            df_velocity = mouse_movement_data
        else:
            df_velocity = self.mouse_movement_data[['x_position', 'y_position', 'time']]

        # Calcular as diferenças de posição e tempo
        df_velocity = df_velocity[['x_position', 'y_position', 'time']]
        df_velocity = df_velocity.sort_values(by='time')

        df_velocity['delta_x'] = df_velocity['x_position'].diff()
        df_velocity['delta_y'] = df_velocity['y_position'].diff()
        df_velocity['delta_t'] = df_velocity['time'].diff()

        # Calcular as velocidades
        df_velocity['velocidade_x'] = df_velocity['delta_x'] / df_velocity['delta_t']
        df_velocity['velocidade_y'] = df_velocity['delta_y'] / df_velocity['delta_t']
        df_velocity['velocidade'] = np.sqrt(df_velocity['velocidade_x'] ** 2 + df_velocity['velocidade_y'] ** 2)

        # Calcular as velocidades médias, máximas e mínimas
        up_average_speed = df_velocity[df_velocity['velocidade_y'] > 0]['velocidade_y'].mean()
        self.up_average_speed = np.nanmean(
            [self.up_average_speed, up_average_speed]) if self.up_average_speed is not None else up_average_speed

        down_average_speed = df_velocity[df_velocity['velocidade_y'] < 0]['velocidade_y'].mean()
        self.down_average_speed = np.nanmean([self.down_average_speed,
                                              down_average_speed]) if self.down_average_speed is not None else down_average_speed

        right_average_speed = df_velocity[df_velocity['velocidade_x'] > 0]['velocidade_x'].mean()
        self.right_average_speed = np.nanmean([self.right_average_speed,
                                               right_average_speed]) if self.right_average_speed is not None else right_average_speed

        left_average_speed = df_velocity[df_velocity['velocidade_x'] < 0]['velocidade_x'].mean()
        self.left_average_speed = np.nanmean([self.left_average_speed,
                                              left_average_speed]) if self.left_average_speed is not None else left_average_speed

        vertical_average_speed = df_velocity['velocidade_y'].abs().mean()
        self.vertical_average_speed = np.nanmean([self.vertical_average_speed,
                                                  vertical_average_speed]) if self.vertical_average_speed is not None else vertical_average_speed

        horizontal_average_speed = df_velocity['velocidade_x'].abs().mean()
        self.horizontal_average_speed = np.nanmean([self.horizontal_average_speed,
                                                    horizontal_average_speed]) if self.horizontal_average_speed is not None else horizontal_average_speed

        average_speed = df_velocity['velocidade'].mean()
        self.average_speed = np.nanmean(
            [self.average_speed, average_speed]) if self.average_speed is not None else average_speed

        maximum_horizontal_speed = df_velocity['velocidade_x'].abs().max()
        self.maximum_horizontal_speed = np.nanmean([self.maximum_horizontal_speed,
                                                    maximum_horizontal_speed]) if self.maximum_horizontal_speed is not None else maximum_horizontal_speed

        maximum_vertical_speed = df_velocity['velocidade_y'].abs().max()
        self.maximum_vertical_speed = np.nanmean([self.maximum_vertical_speed,
                                                  maximum_vertical_speed]) if self.maximum_vertical_speed is not None else maximum_vertical_speed

        minimum_horizontal_speed = df_velocity[df_velocity['velocidade_x'] != 0]['velocidade_x'].abs().min()
        self.minimum_horizontal_speed = np.nanmean([self.minimum_horizontal_speed,
                                                    minimum_horizontal_speed]) if self.minimum_horizontal_speed is not None else minimum_horizontal_speed

        minimum_vertical_speed = df_velocity[df_velocity['velocidade_y'] != 0]['velocidade_y'].abs().min()
        self.minimum_vertical_speed = np.nanmean([self.minimum_vertical_speed,
                                                  minimum_vertical_speed]) if self.minimum_vertical_speed is not None else minimum_vertical_speed

        maximum_speed = df_velocity['velocidade'].max()
        self.maximum_speed = np.nanmean(
            [self.maximum_speed, maximum_speed]) if self.maximum_speed is not None else maximum_speed

        minimum_speed = df_velocity[df_velocity['velocidade'] != 0]['velocidade'].min()
        self.minimum_speed = np.nanmean(
            [self.minimum_speed, minimum_speed]) if self.minimum_speed is not None else minimum_speed

        return [self.up_average_speed, self.down_average_speed, self.right_average_speed, self.left_average_speed,
                self.vertical_average_speed, self.horizontal_average_speed, self.average_speed,
                self.maximum_horizontal_speed, self.maximum_vertical_speed, self.minimum_horizontal_speed,
                self.minimum_vertical_speed, self.maximum_speed, self.minimum_speed]

    def extract_movement_metrics(self, mouse_movement_data: pd.DataFrame = None) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, como quantidade de movimentos, direções, etc.
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
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

        # Contar os movimentos
        up_moves = (df_movement['mudanca_y'] > 0).sum()
        self.up_moves = np.nanmean([self.up_moves, up_moves]) if self.up_moves is not None else up_moves

        down_moves = (df_movement['mudanca_y'] < 0).sum()
        self.down_moves = np.nanmean([self.down_moves, down_moves]) if self.down_moves is not None else down_moves

        right_moves = (df_movement['mudanca_x'] > 0).sum()
        self.right_moves = np.nanmean([self.right_moves, right_moves]) if self.right_moves is not None else right_moves

        left_moves = (df_movement['mudanca_x'] < 0).sum()
        self.left_moves = np.nanmean([self.left_moves, left_moves]) if self.left_moves is not None else left_moves

        horizontal_moves = self.right_moves + self.left_moves
        self.horizontal_moves = np.nanmean(
            [self.horizontal_moves, horizontal_moves]) if self.horizontal_moves is not None else horizontal_moves

        vertical_moves = self.up_moves + self.down_moves
        self.vertical_moves = np.nanmean(
            [self.vertical_moves, vertical_moves]) if self.vertical_moves is not None else vertical_moves

        return [self.up_moves, self.down_moves, self.right_moves, self.left_moves, self.horizontal_moves,
                self.vertical_moves]

    def extract_distance_metrics(self, mouse_movement_data: pd.DataFrame = None) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, distância percorrida pelo ponteiro em cada direção.
        :param mouse_movement_data: Dataframe de dados de evento 'move' do mouse
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

        # Calcular as distâncias
        horizontal_distance = df_distance['diff_x'].abs().sum()
        self.horizontal_distance = np.nanmean([self.horizontal_distance,
                                               horizontal_distance]) if self.horizontal_distance is not None else horizontal_distance

        vertical_distance = df_distance['diff_y'].abs().sum()
        self.vertical_distance = np.nanmean(
            [self.vertical_distance, vertical_distance]) if self.vertical_distance is not None else vertical_distance

        total_distance = np.sqrt(df_distance['diff_x'] ** 2 + df_distance['diff_y'] ** 2).sum()
        self.total_distance = np.nanmean(
            [self.total_distance, total_distance]) if self.total_distance is not None else total_distance

        # Calcular as distâncias para cima, para baixo, para a esquerda e para a direita
        up_distance = df_distance[df_distance['diff_y'] > 0]['diff_y'].sum()
        self.up_distance = np.nanmean([self.up_distance, up_distance]) if self.up_distance is not None else up_distance

        down_distance = -df_distance[df_distance['diff_y'] < 0]['diff_y'].sum()
        self.down_distance = np.nanmean(
            [self.down_distance, down_distance]) if self.down_distance is not None else down_distance

        right_distance = df_distance[df_distance['diff_x'] > 0]['diff_x'].sum()
        self.right_distance = np.nanmean(
            [self.right_distance, right_distance]) if self.right_distance is not None else right_distance

        left_distance = -df_distance[df_distance['diff_x'] < 0]['diff_x'].sum()
        self.left_distance = np.nanmean(
            [self.left_distance, left_distance]) if self.left_distance is not None else left_distance

        return [self.horizontal_distance, self.vertical_distance, self.total_distance, self.up_distance,
                self.down_distance, self.right_distance, self.left_distance]

    def extract_clicks_metrics(self, mouse_click_data: pd.DataFrame = None) -> list[Any]:
        """
        Realiza a extração dos dados e métricas do mouse, clicks, velocidade de click, etc.
        :param mouse_movement_data: Dataframe de dados de evento 'click' do mouse
        :return: Lista com todas as métricas extraídas da leitura dos dados
        """
        if mouse_click_data is not None:
            df_clicks = mouse_click_data
        else:
            df_clicks = self.mouse_click_data[['x_position', 'y_position', 'button', 'status', 'time']]

        df_clicks = df_clicks.sort_values(by='time')

        # Calcular o número total de cliques
        total_clicks = df_clicks[df_clicks['status'] == ClickStatus.PRESS.value].shape[0]
        self.total_clicks = np.nanmean([self.total_clicks, total_clicks]) if self.total_clicks is not None else total_clicks

        # Calcular o número de cliques direitos e esquerdos
        right_clicks = df_clicks[
            (df_clicks['button'] == str(Button.right)) & (df_clicks['status'] == ClickStatus.PRESS.value)].shape[0]
        self.right_clicks = np.nanmean([self.right_clicks, right_clicks]) if self.right_clicks is not None else right_clicks

        left_clicks = df_clicks[
            (df_clicks['button'] == str(Button.left)) & (df_clicks['status'] == ClickStatus.PRESS.value)].shape[0]
        self.left_clicks = np.nanmean([self.left_clicks, left_clicks]) if self.left_clicks is not None else left_clicks

        click_pairs = pd.DataFrame(columns=['button', 'press_time', 'release_time'])

        # Encontra os pares 'press' e 'release' para o mesmo botão
        for button in [Button.right, Button.left]:
            press_times = \
                df_clicks[(df_clicks['button'] == str(button)) & (df_clicks['status'] == ClickStatus.PRESS.value)][
                    'time']
            release_times = \
                df_clicks[
                    (df_clicks['button'] == str(button)) & (df_clicks['status'] == ClickStatus.RELEASE.value)][
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
        self.right_click_total_duration = np.nanmean([self.right_click_total_duration, right_click_total_duration]) if self.right_click_total_duration is not None else right_click_total_duration

        left_click_total_duration = click_pairs[click_pairs['button'] == str(Button.left)]['duration'].sum()
        self.left_click_total_duration = np.nanmean([self.left_click_total_duration, left_click_total_duration]) if self.left_click_total_duration is not None else left_click_total_duration

        right_click_average_duration = click_pairs[click_pairs['button'] == str(Button.right)]['duration'].mean()
        self.right_click_average_duration = np.nanmean([self.right_click_average_duration, right_click_average_duration]) if self.right_click_average_duration is not None else right_click_average_duration

        left_click_average_duration = click_pairs[click_pairs['button'] == str(Button.left)]['duration'].mean()
        self.left_click_average_duration = np.nanmean([self.left_click_average_duration, left_click_average_duration]) if self.left_click_average_duration is not None else left_click_average_duration

        return [self.total_clicks, self.right_clicks, self.left_clicks, self.right_click_total_duration,
                self.left_click_total_duration, self.right_click_average_duration, self.left_click_average_duration]


if __name__ == '__main__':
    analyses = MouseAnalyses()
    list_mouse_movement_data, list_mouse_click_data = read_file('../../files/user/mouse_data.json')

    for move_data in list_mouse_movement_data:
        analyses.mouse_movement_data = move_data

        analyses.extract_velocity_metrics()
        analyses.extract_movement_metrics()
        analyses.extract_distance_metrics()

    for click_data in list_mouse_click_data:
        analyses.mouse_click_data = click_data
        analyses.extract_clicks_metrics()

