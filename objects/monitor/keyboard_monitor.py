from pynput.keyboard import Key, KeyCode
from pynput import keyboard
import time


class KeyboardMonitor:
    """
    Classe responsável por realizar a gravação dos dados do teclado do usuário. Os dados gravados são armazeanos em uma estrutura que possui o seguinte formato:
    'press': Dados de teclas pressionadas, contendo a tecla pressionada e o tempo em que o evento ocorreu
    'release': Dados de teclas soltas, contendo a tecla que foi solta e o tempo em que o evento ocorreu
    """
    def __init__(self):
        self.start_time = time.time()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.stop_flag = False
        self.recorded_data = {"press": [], "release": []}

    def on_press(self, key: Key | KeyCode) -> None:
        """
        Evento de tecla pressionada, dispara a gravação do dado na estrtura 'press'
        :param key: Tecla que foi pressionada
        :return:
        """
        if self.stop_flag:
            return False
        elapsed_time = time.time() - self.start_time
        self.recorded_data["press"].append({"key": str(key), "time": elapsed_time})

    def on_release(self, key: Key | KeyCode) -> None:
        """
        Evento de tecla solta, dispara a gravação do dado na estrutura 'release'
        :param key: Tecla que foi solta
        :return:
        """
        if self.stop_flag:
            return False
        elapsed_time = time.time() - self.start_time
        self.recorded_data["release"].append({"key": str(key), "time": elapsed_time})

    def start(self) -> None:
        """
        Dispara o início da gravação dos eventos
        :return:
        """
        with self.listener as listener:
            listener.join()

    def stop(self) -> dict:
        """
        Encerra a gração de dados
        :return: Dicionário com os eventos 'press' e 'release'
        """
        self.stop_flag = True
        return self.recorded_data


if __name__ == '__main__':
    monitor = KeyboardMonitor()
    monitor.start()
    # Quando você quiser parar a execução, você pode chamar:
    # monitor.stop()
    # E para acessar os dados, você pode usar:
    # print(monitor.recorded_data)
