import os

from common.constants import BASE_DIR


class UserService:
    def __init__(self):
        self.base_path = os.path.join(BASE_DIR, 'files')

    def get_user_data(self, username: str = None):
        if username is not None:
            user_data = {'data': {}}
            user_path = os.path.join(self.base_path, username)
            if os.path.exists(user_path):
                user_files = os.listdir(user_path)
                user_data["username"] = username
                user_data["files"] = user_files
            else:
                user_data = {"error": "Usuário não encontrado"}
        else:
            user_data = {'data': []}
            for username in os.listdir(self.base_path):
                user_path = os.path.join(self.base_path, username)
                user_files = os.listdir(user_path)
                user_data['data'].append({
                    "username": username,
                    "files": user_files
                })
        return user_data

    def get_user_list(self):
        user_data = {'data': []}
        for username in os.listdir(self.base_path):
            user_data['data'].append({'username': username})
        return user_data
