from flask import Flask
from flask_cors import CORS

from application.backend.controllers.keyboard_data_controller import KeyboardViewController
from application.backend.controllers.mouse_view_controller import MouseViewController
from application.backend.controllers.record_controller import RecordController
from application.backend.controllers.statistics_controller import StatisticsController
from application.backend.controllers.user_controller import UserController
from application.backend.controllers.activity_controller import ActivityController
from application.backend.controllers.model_controller import ModelController

app = Flask(__name__)
CORS(app)

app.add_url_rule('/check_user', view_func=UserController.check_user, methods=['GET'])
app.add_url_rule('/check_user/<username>', view_func=UserController.check_user, methods=['GET'])
app.add_url_rule('/users_list', view_func=UserController.user_list, methods=['GET'])
app.add_url_rule('/activities', view_func=ActivityController.activity_list, methods=['GET'])
app.add_url_rule('/models', view_func=ModelController.model_list, methods=['GET'])

app.add_url_rule('/view/mouse_position/<username>/<activity>', view_func=MouseViewController.mouse_position, methods=['GET'])
app.add_url_rule('/view/mouse_click/<username>/<activity>', view_func=MouseViewController.mouse_click, methods=['GET'])
app.add_url_rule('/view/mouse_full/<username>/<activity>', view_func=MouseViewController.mouse_full, methods=['GET'])
app.add_url_rule('/view/keyboard_full/<username>/<activity>', view_func=KeyboardViewController.keyboard_full, methods=['GET'])

app.add_url_rule('/view/mouse_position/<username>', view_func=MouseViewController.mouse_position, methods=['GET'])
app.add_url_rule('/view/mouse_click/<username>', view_func=MouseViewController.mouse_click, methods=['GET'])
app.add_url_rule('/view/mouse_full/<username>', view_func=MouseViewController.mouse_full, methods=['GET'])
app.add_url_rule('/view/keyboard_full/<username>', view_func=KeyboardViewController.keyboard_full, methods=['GET'])

app.add_url_rule('/stats/keyboard', view_func=StatisticsController.get_keyboard_statistics, methods=['GET'])
app.add_url_rule('/stats/mouse', view_func=StatisticsController.get_mouse_statistics, methods=['GET'])
app.add_url_rule('/stats/full', view_func=StatisticsController.get_full_statistics, methods=['GET'])
app.add_url_rule('/stats/keyboard/<username>', view_func=StatisticsController.get_keyboard_statistics, methods=['GET'])
app.add_url_rule('/stats/mouse/<username>', view_func=StatisticsController.get_mouse_statistics, methods=['GET'])
app.add_url_rule('/stats/full/<username>', view_func=StatisticsController.get_full_statistics, methods=['GET'])
app.add_url_rule('/stats/keyboard/<username>/<activity>', view_func=StatisticsController.get_keyboard_statistics, methods=['GET'])
app.add_url_rule('/stats/mouse/<username>/<activity>', view_func=StatisticsController.get_mouse_statistics, methods=['GET'])
app.add_url_rule('/stats/full/<username>/<activity>', view_func=StatisticsController.get_full_statistics, methods=['GET'])

app.add_url_rule('/start_recording', view_func=RecordController.start_recording, methods=['POST'])
app.add_url_rule('/stop_recording', view_func=RecordController.stop_recording, methods=['POST'])

app.add_url_rule('/models', view_func=ModelController.execute_model, methods=['POST'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
