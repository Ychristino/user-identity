import json
import os

from common.constants import KEYBOARD_FILE, MOUSE_FILE, BASE_DIR


class DataService:
    def __init__(self):
        self.base_path = os.path.join(BASE_DIR, 'files')

    def get_mouse_position_data(self, username: str):
        user_path = os.path.join(self.base_path, username, MOUSE_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                return {'data': [node['move'] for node in data][0]}
        return {'data': ''}

    def get_mouse_click_data(self, username: str):
        user_path = os.path.join(self.base_path, username, MOUSE_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                return {'data': [node['click'] for node in data][0]}
        return {}

    def get_mouse_full_data(self, username: str):
        user_path = os.path.join(self.base_path, username, MOUSE_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                return {'data': data}
        return {}

    def get_keyboard_full_data(self, username: str):
        user_path = os.path.join(self.base_path, username, KEYBOARD_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                return {'data': data}
        return {}
