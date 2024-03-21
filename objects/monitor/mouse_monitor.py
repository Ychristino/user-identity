from pynput import mouse
import time

from common.click_status import ClickStatus


class MouseMonitor:
    """
    Classe responsável por realizar a gravação dos dados do mouse do usuário. Os dados gravados são armazeanos em uma
    estrutura que possui o seguinte formato: 'move': Dados de coordenada do mouse ('x' e 'y') e o tempo em que o
    evento ocorreu 'click': Dados de coordenada do mouse ('x' e 'y'), botão do mouse, estado do botão (solto ou
    pressionado) e o tempo em que o evento ocorreu
    """
    def __init__(self):
        self.start_time = time.time()
        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.stop_flag = False
        self.recorded_data = {"move": [], "click": []}

    def on_move(self, x: int, y: int) -> bool:
        """
        Evento de movimentação do ponteiro, dispara a gravação do dado na estrutura 'move'.
        :param x: Posição 'X' (horizontal) do ponteiro
        :param y: Posição 'Y' (vertical) do ponteiro
        :return:
        """
        if self.stop_flag:
            return False
        elapsed_time = time.time() - self.start_time
        self.recorded_data["move"].append({"x_position": x, "y_position": y, "time": elapsed_time})

    def on_click(self, x: int, y: int, button, pressed) -> bool:
        """
        Evento de click do mouse, dispara a gravação do dado na estrutura 'click'
        :param x: Posição 'X' (horizontal) do ponteiro
        :param y: Posição 'Y' (vertical) do ponteiro
        :param button: Botão que disparou o evento (Click direito ou esquerdo)
        :param pressed: Estado do botão, pressionado ou solto
        :return:
        """
        if self.stop_flag:
            return False
        elapsed_time = time.time() - self.start_time
        self.recorded_data["click"].append(
            {"x_position": x, "y_position": y, "button": str(button), "status": ClickStatus.PRESS.value if pressed else ClickStatus.RELEASE.value,
             "time": elapsed_time})

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
        :return: Dicionário com os eventos 'move' e 'click'
        """
        self.stop_flag = True
        return self.recorded_data


if __name__ == '__main__':
    monitor = MouseMonitor()
    monitor.start()
    # Quando você quiser parar a execução, você pode chamar:
    # monitor.stop()
    # E para acessar os dados, você pode usar:
    # print(monitor.data)
