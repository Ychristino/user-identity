from application.backend.main_api import app as app_api

if __name__ == "__main__":
    app_api.run(port=5000)