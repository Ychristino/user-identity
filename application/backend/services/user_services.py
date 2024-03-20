import os



class UserService:
    def __init__(self):
        self.base_path = ".\\files"

    def get_user_data(self, username: str = None):
        user_data = {}
        if username:
            user_path = os.path.join(self.base_path, username)
            if os.path.exists(user_path):
                user_files = os.listdir(user_path)
                user_data["username"] = username
                user_data["files"] = user_files
            else:
                user_data = {"error": "Usuário não encontrado"}
        else:
            for username in os.listdir(self.base_path):
                user_path = os.path.join(self.base_path, username)
                user_files = os.listdir(user_path)
                user_data[username] = {
                    "username": username,
                    "files": user_files
                }
        return user_data

    def get_user_list(self):
        user_data = []
        for username in os.listdir(self.base_path):
            user_data.append({'username': username})
        return user_data
