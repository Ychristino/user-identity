from flask import jsonify, request

from application.backend.services.model_service import ModelService
from common.activity import find_activity_by_value
from common.models import find_model_by_value, Models

model_service = ModelService()


class ModelController:

    @staticmethod
    def model_list():
        return jsonify(model_service.get_model_list()), 200

    @staticmethod
    def execute_model():
        data = request.json

        selected_model = find_model_by_value(data.get('model'))
        selected_activity = None

        if not isinstance(selected_model, Models):
            return jsonify({"error": "Model information was not found."}), 400

        if data.get('activity') is not None:
            selected_activity = find_activity_by_value(data.get('activity'))

        return jsonify(model_service.execute_model(selected_model, selected_activity)), 200
