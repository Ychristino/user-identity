import os
import time
import threading
import json
import inspect
from typing import Tuple, List, Any

from common.activity import Activity
from common.constants import MOUSE_FILE, KEYBOARD_FILE, BASE_DIR
from objects.monitor.keyboard_monitor import KeyboardMonitor
from objects.monitor.mouse_monitor import MouseMonitor


class RecordData:
    """
    Classe responsável por realizar a gravação dos dados conforme a estrutura completa. Capaz de realizar a gravação
    de eventos de mouse, teclado ou ambos. Apenas gerencia os processos, as estruturas e processos devem ser
    agrupadas em classes independentes de monitoramente, como mouse_monitor ou keyboard_monitor
    """

    def __init__(self, username: str, activity: Activity):
        self.username = username
        self.activity = activity
        self.mouse_monitor = MouseMonitor()
        self.keyboard_monitor = KeyboardMonitor()
        self.mouse_data = []
        self.keyboard_data = []

    def record_mouse(self) -> None:
        """
        Dispara a gravação dos eventos de mouse
        :return:
        """
        self.mouse_monitor.start()

    def record_keyboard(self) -> None:
        """
        Dispara a gravação dos eventos de teclado
        :return:
        """
        self.keyboard_monitor.start()

    def stop_mouse_record(self) -> dict:
        """
        Encerra a execução dos eventos de mouse
        :return: Estrutura de gravação dos eventos de mouse
        """
        self.mouse_data = self.mouse_monitor.stop()
        self.export_data()
        return self.mouse_data

    def stop_keyboard_record(self) -> dict:
        """
        Encerra a execuçã dos eventos de teclado
        :return: Estrutura de gravação dos eventos de teclado
        """
        self.keyboard_data = self.keyboard_monitor.stop()
        self.export_data()
        return self.keyboard_data

    def record_all(self) -> None:
        """
        Inicia a gravação de todos os eventos (mouse e teclado)
        :return:
        """
        threading.Thread(target=self.record_mouse).start()
        threading.Thread(target=self.record_keyboard).start()

    def stop_all(self) -> tuple[dict, dict]:
        """
        Encerra a execução de todos os eventos (mouse e teclado)
        :return: Estruturas de gravação dos eventos de mouse e teclado, respectivamente
        """
        return self.stop_mouse_record(), self.stop_keyboard_record()

    def export_data(self) -> None:
        """
        Realiza a gravação dos arquivos de eventos de mouse e teclado
        :return:
        """
        caller_method = inspect.stack()[1][3]
        data_path = os.path.join(BASE_DIR, 'files', self.username, self.activity.value['folder'])

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        if bool(self.mouse_data):
            if caller_method == 'stop_mouse_record' or caller_method == 'stop_all':
                file_path = os.path.join(data_path, MOUSE_FILE)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                else:
                    data = []
                data.append(self.mouse_data)
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)

        if bool(self.keyboard_data):
            if caller_method == 'stop_keyboard_record' or caller_method == 'stop_all':
                file_path = os.path.join(data_path,KEYBOARD_FILE)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                else:
                    data = []
                data.append(self.keyboard_data)
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)


if __name__ == '__main__':
    record_data = RecordData('user')
    recording_thread = threading.Thread(target=record_data.record_all)
    recording_thread.start()
    time.sleep(10)
    record_data.stop_all()
    recording_thread.join()
