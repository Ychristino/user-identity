from flask import jsonify

from application.backend.services.activity_service import ActivityService

activity_service = ActivityService()


class ActivityController:

    @staticmethod
    def activity_list():
        return jsonify(activity_service.get_activity_list()), 200
