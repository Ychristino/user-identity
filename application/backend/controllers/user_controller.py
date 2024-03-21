from flask import jsonify
from application.backend.services.user_services import UserService

user_service = UserService()


class UserController:
    @staticmethod
    def check_user(username: str = None):
        return jsonify(user_service.get_user_data(username))

    @staticmethod
    def user_list():
        return jsonify(user_service.get_user_list())
