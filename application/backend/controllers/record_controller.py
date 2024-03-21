from flask import jsonify, request
from application.backend.services.record_service import RecordService

record_service = RecordService()


class RecordController:
    @staticmethod
    def start_recording():
        data = request.json
        if data.get('main_user'):
            user_running = 'user'
        else:
            user_running = data.get('user_running')

        if user_running:
            if record_service.start_record(user_running):
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
