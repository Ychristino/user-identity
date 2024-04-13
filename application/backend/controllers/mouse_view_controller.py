from flask import jsonify
from application.backend.services.data_service import DataService

data_service = DataService()


class MouseViewController:
    @staticmethod
    def mouse_position(username: str, activity: str = None):
        return jsonify(data_service.get_mouse_position_data(username, activity))

    @staticmethod
    def mouse_click(username: str, activity: str = None):
        return jsonify(data_service.get_mouse_click_data(username, activity))

    @staticmethod
    def mouse_full(username: str, activity: str = None):
        return jsonify(data_service.get_mouse_full_data(username, activity))
