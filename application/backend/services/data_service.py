import json
import os

from common.constants import KEYBOARD_FILE, MOUSE_FILE, BASE_DIR


class DataService:
    def __init__(self):
        self.base_path = os.path.join(BASE_DIR, 'files')

    def get_mouse_position_data(self, username: str):
        return_data = {'data': []}
        user_path = os.path.join(self.base_path, username, MOUSE_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                for json_object in data:
                    return_data['data'] += json_object['move']
        return return_data

    def get_mouse_click_data(self, username: str):
        return_data = {'data': []}
        user_path = os.path.join(self.base_path, username, MOUSE_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                for json_object in data:
                    return_data['data'] += json_object['click']
        return return_data

    def get_mouse_full_data(self, username: str):
        return_data = {'data': {
            'move': [],
            'click': []
        }}
        user_path = os.path.join(self.base_path, username, MOUSE_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                for json_object in data:
                    return_data['data']['move'] += json_object['move']
                    return_data['data']['click'] += json_object['click']
        return return_data

    def get_keyboard_full_data(self, username: str):
        return_data = {'data': {
            'press': [],
            'release': []
        }}
        user_path = os.path.join(self.base_path, username, KEYBOARD_FILE)
        if os.path.exists(user_path):
            with open(user_path, 'r') as f:
                data = json.load(f)
                for json_object in data:
                    return_data['data']['press'] += json_object['press']
                    return_data['data']['release'] += json_object['release']
        return return_data

