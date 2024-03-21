from flask import jsonify, request

from application.backend.services.statistics_service import StatisticsService

statistic_service = StatisticsService()


class StatisticsController:

    @staticmethod
    def get_mouse_statistics(username: str = None):
        return jsonify(statistic_service.get_mouse_statistics(username=username)), 200

    @staticmethod
    def get_keyboard_statistics(username: str = None):
        return jsonify(statistic_service.get_keyboard_statistics(username=username)), 200

    @staticmethod
    def get_full_statistics(username: str = None):
        return jsonify(statistic_service.get_full_statistics(username=username)), 200
