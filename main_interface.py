import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_flask_app(app, port):
    app.run(port=port)


if __name__ == "__main__":
    from application.backend.main_api import app as app_api  # Importa o objeto Flask do backend
    from application.frontend.main_front import app as app_interface  # Importa o objeto Flask do frontend

    api_port = 5000
    interface_port = 5001

    webbrowser.open("http://127.0.0.1:5001")
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_api = executor.submit(run_flask_app, app_api, api_port)
        future_interface = executor.submit(run_flask_app, app_interface, interface_port)

        # Espera que ambas as threads terminem
        for future in as_completed([future_api, future_interface]):
            try:
                future.result()  # Aguarda o término da execução da thread
            except Exception as e:
                print(f"Erro ao iniciar aplicativo: {e}")

    print("Ambos os aplicativos foram iniciados com sucesso.")
