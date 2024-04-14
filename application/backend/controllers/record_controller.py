from flask import jsonify, request
from application.backend.services.record_service import RecordService
from common.activity import find_activity_by_value, Activity

record_service = RecordService()


class RecordController:
    @staticmethod
    def start_recording():
        data = request.json

        selected_activity = find_activity_by_value(data.get('activity'))

        if data.get('main_user'):
            user_running = 'user'
        else:
            user_running = data.get('user_running')
        if not isinstance(selected_activity, Activity):
            return jsonify({"error": "Activity information was not found."}), 400

        if user_running:
            if record_service.start_record(user_running, selected_activity):
                return jsonify({"message": f"Recording started for {str(user_running)}"}), 200
            else:
                return jsonify({"error": "Recording is already in progress"}), 400
        else:
            return jsonify({"error": "No user information was found."}), 400

    @staticmethod
    def stop_recording():
        if record_service.stop_record():
            return jsonify({"message": "Recording stopped successfully"}), 200
        else:
            return jsonify({"message": "No recording in progress"}), 400
