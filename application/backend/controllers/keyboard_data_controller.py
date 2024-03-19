from flask import jsonify
from application.backend.services.data_service import DataService

data_service = DataService()


class KeyboardViewController:
    @staticmethod
    def keyboard_full(username: str):
        return jsonify(data_service.get_keyboard_full_data(username))
